from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import logging

logger = logging.getLogger(__name__)

from .models import (
    Subject, Task, TaskMessage, Note, StudyStreak, LearningGoal,
    StudySession, Topic, Platform, PlatformAccount,
    UserStats, DailyActivity, Resource
)

from .forms import (
    SignupForm, SubjectForm, TaskForm, NoteForm,
    LearningGoalForm, StudySessionForm, GitHubUsernameForm
)

from core.services.groq import generate_goal_solution, generate_task_ai_reply
from core.services.resources import seed_resources_by_goal


# ==================================================
# AUTH
# ==================================================

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"]
            )
            login(request, user)
            return redirect("dashboard")
    else:
        form = SignupForm()
    return render(request, "core/signup.html", {"form": form})


def login_view(request):
    error = ""
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )
        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            error = "Invalid credentials"
    return render(request, "core/login.html", {"error": error})


def logout_view(request):
    logout(request)
    return redirect("login")


# ==================================================
# DASHBOARD
# ==================================================

@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)
    completed = tasks.filter(completed=True).count()
    total = tasks.count()
    progress = int((completed / total) * 100) if total else 0

    streak, _ = StudyStreak.objects.get_or_create(user=request.user)
    today = timezone.now().date()

    today_minutes = StudySession.objects.filter(
        user=request.user,
        study_date=today
    ).aggregate(Sum("duration_minutes"))["duration_minutes__sum"] or 0

    return render(request, "core/dashboard.html", {
        "tasks": tasks,
        "total_tasks": total,
        "completed_count": completed,
        "pending_count": total - completed,
        "progress": progress,
        "streak": streak,
        "today": today,
        "today_minutes": today_minutes,
    })


# ==================================================
# TASKS
# ==================================================

@login_required
def tasks_hub(request):
    tasks = Task.objects.filter(user=request.user).order_by("-created_at")

    if request.method == "POST":
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            # FIX: needs_help field now exists in model
            if task.task_type == "assignment" and task.material:
                task.needs_help = True
            task.save()
            messages.success(request, "Task created successfully!")
            return redirect("tasks_hub")
    else:
        form = TaskForm()

    total = tasks.count()
    completed = tasks.filter(completed=True).count()

    return render(request, "core/tasks_hub.html", {
        "form": form,
        "tasks": tasks,
        "total": total,
        "completed": completed,
        "pending": total - completed,
        "progress": int((completed / total) * 100) if total else 0,
    })


@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = not task.completed
    task.save()
    if task.completed:
        _update_streak(request.user)
    return redirect("tasks_hub")


@login_required
def task_detail(request, task_id):
    """View for task details and AI-assisted chat."""
    task = get_object_or_404(Task, id=task_id, user=request.user)
    chat_messages = task.messages.all()

    if request.method == "POST":
        user_msg = request.POST.get("message", "").strip()
        if user_msg:
            TaskMessage.objects.create(task=task, sender="user", content=user_msg)

            try:
                ai_reply = generate_task_ai_reply(task, user_msg)
            except Exception as e:
                logger.error(f"AI response failed for task {task_id}: {str(e)}", exc_info=True)
                ai_reply = "AI is temporarily unavailable. Please try again later."
                messages.error(request, "Could not generate AI response. Please check your API keys.")

            TaskMessage.objects.create(task=task, sender="ai", content=ai_reply)
            task.ai_solution = ai_reply
            task.needs_help = False
            task.save(update_fields=["ai_solution", "needs_help"])

        return redirect("task_detail", task_id=task.id)

    return render(request, "core/task_detail.html", {
        "task": task,
        "messages": chat_messages,
    })


@login_required
def task_need_help(request, task_id):
    """Generate AI assistance for a task."""
    task = get_object_or_404(Task, id=task_id, user=request.user)

    prompt = (
        f"User needs help with this task.\n\n"
        f"Title: {task.title}\n"
        f"Subject: {task.custom_subject or task.subject}\n"
        f"Type: {task.get_task_type_display()}\n"
        f"Deadline: {task.deadline or 'Not set'}\n"
        f"Estimated hours: {task.estimated_hours or 'Not set'}"
    )

    try:
        ai_reply = generate_task_ai_reply(task, prompt)
    except Exception as e:
        logger.error(f"AI help generation failed for task {task_id}: {str(e)}", exc_info=True)
        ai_reply = "AI is temporarily unavailable. Please try again later."
        messages.error(request, "Could not generate AI help. Please check your API keys.")

    TaskMessage.objects.create(task=task, sender="ai", content=ai_reply)
    task.ai_solution = ai_reply
    task.needs_help = False
    task.save(update_fields=["ai_solution", "needs_help"])

    return redirect("task_detail", task_id=task.id)


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        messages.success(request, "Task deleted.")
    return redirect("tasks_hub")


# ==================================================
# NOTES
# ==================================================

@login_required
def add_note(request):
    if request.method == "POST":
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, "Note saved!")
            return redirect("my_notes")
    else:
        form = NoteForm()

    return render(request, "core/add_note.html", {"form": form})


@login_required
def my_notes(request):
    return render(request, "core/my_notes.html", {
        "my_notes": Note.objects.filter(user=request.user)
    })


@login_required
def public_library(request):
    notes = Note.objects.filter(visibility="public").exclude(user=request.user)
    return render(request, "core/public_library.html", {"notes": notes})


# ==================================================
# PROFILE
# ==================================================

@login_required
def profile(request):
    stats, _ = UserStats.objects.get_or_create(user=request.user)

    github = PlatformAccount.objects.filter(
        user=request.user, platform__slug="github"
    ).first()

    leetcode = PlatformAccount.objects.filter(
        user=request.user, platform__slug="leetcode"
    ).first()

    gfg = PlatformAccount.objects.filter(
        user=request.user, platform__slug="gfg"
    ).first()

    codechef = PlatformAccount.objects.filter(
        user=request.user, platform__slug="codechef"
    ).first()

    hackerrank = PlatformAccount.objects.filter(
        user=request.user, platform__slug="hackerrank"
    ).first()

    context = {
        "stats": stats,
        "total_xp": stats.total_xp,
        "level": stats.level,
        "github": github,
        "github_commits": stats.total_commits,
        "github_repos": stats.github_repos,
        "leetcode": leetcode,
        "leetcode_solved": stats.leetcode_solved,
        "leetcode_xp": stats.leetcode_xp,
        "gfg": gfg,
        "gfg_solved": stats.gfg_solved,
        "gfg_xp": stats.gfg_xp,
        "codechef": codechef,
        "codechef_solved": stats.codechef_solved,
        "codechef_xp": stats.codechef_xp,
        "hackerrank": hackerrank,
        "hackerrank_solved": stats.hackerrank_solved,
        "hackerrank_xp": stats.hackerrank_xp,
    }

    return render(request, "core/profile.html", context)


# ==================================================
# PLATFORM CONNECT / SYNC
# FIX: removed duplicate add_github_username and sync_github definitions.
#      Only one canonical version of each now exists.
# ==================================================

@login_required
def add_github_username(request):
    platform, _ = Platform.objects.get_or_create(
        slug="github",
        defaults={"name": "GitHub", "base_url": "https://github.com"}
    )

    if request.method == "POST":
        form = GitHubUsernameForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            PlatformAccount.objects.update_or_create(
                user=request.user,
                platform=platform,
                defaults={
                    "username": username,
                    "profile_url": f"https://github.com/{username}",
                }
            )
            stats, _ = UserStats.objects.get_or_create(user=request.user)
            stats.github_username = username
            stats.save(update_fields=["github_username"])
            messages.success(request, f"GitHub account @{username} connected!")
            return redirect("profile")
    else:
        form = GitHubUsernameForm()

    return render(request, "core/add_github.html", {"form": form})


@login_required
def sync_github(request):
    account = get_object_or_404(
        PlatformAccount, user=request.user, platform__slug="github"
    )
    try:
        from core.services.github import sync_github_activity
        sync_github_activity(account)
        messages.success(request, "GitHub synced successfully!")
    except Exception as e:
        messages.error(request, f"GitHub sync failed: {e}")
    return redirect("profile")


@login_required
def disconnect_github(request):
    PlatformAccount.objects.filter(
        user=request.user, platform__slug="github"
    ).delete()
    stats, _ = UserStats.objects.get_or_create(user=request.user)
    stats.github_username = None
    stats.github_xp = 0
    stats.total_commits = 0
    stats.github_repos = 0
    stats.recalculate_totals()
    messages.success(request, "GitHub disconnected.")
    return redirect("profile")


@login_required
def github_activity(request):
    account = PlatformAccount.objects.filter(
        user=request.user, platform__slug="github"
    ).first()
    stats, _ = UserStats.objects.get_or_create(user=request.user)

    activities = (
        DailyActivity.objects.filter(account=account).order_by("-date")
        if account else []
    )

    return render(request, "core/github_activity.html", {
        "account": account,
        "activities": activities,
        "total_commits": stats.total_commits,
        "total_xp": stats.github_xp,
    })


# ==================================================
# LEETCODE
# ==================================================

@login_required
def add_leetcode(request):
    platform, _ = Platform.objects.get_or_create(
        slug="leetcode",
        defaults={"name": "LeetCode", "base_url": "https://leetcode.com"}
    )

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        if username:
            PlatformAccount.objects.update_or_create(
                user=request.user,
                platform=platform,
                defaults={
                    "username": username,
                    "profile_url": f"https://leetcode.com/{username}",
                }
            )
            stats, _ = UserStats.objects.get_or_create(user=request.user)
            stats.leetcode_username = username
            stats.save(update_fields=["leetcode_username"])
            return redirect("leetcode_sync")

    return render(request, "core/add_leetcode.html")


@login_required
def leetcode_sync(request):
    try:
        from core.services.leetcode import sync_leetcode_by_username
        sync_leetcode_by_username(request.user)
        messages.success(request, "LeetCode synced!")
    except Exception as e:
        messages.error(request, f"LeetCode sync failed: {e}")
    return redirect("profile")


@login_required
def disconnect_leetcode(request):
    PlatformAccount.objects.filter(
        user=request.user, platform__slug="leetcode"
    ).delete()
    stats, _ = UserStats.objects.get_or_create(user=request.user)
    stats.leetcode_solved = 0
    stats.leetcode_xp = 0
    stats.leetcode_username = ""
    stats.leetcode_easy = 0
    stats.leetcode_medium = 0
    stats.leetcode_hard = 0
    stats.save(update_fields=[
        "leetcode_solved", "leetcode_xp", "leetcode_username",
        "leetcode_easy", "leetcode_medium", "leetcode_hard"
    ])
    stats.recalculate_totals()
    messages.success(request, "LeetCode disconnected.")
    return redirect("profile")


# ==================================================
# GFG (GeeksforGeeks)
# ==================================================

@login_required
def add_gfg(request):
    platform, _ = Platform.objects.get_or_create(
        slug="gfg",
        defaults={"name": "GeeksforGeeks", "base_url": "https://www.geeksforgeeks.org"}
    )

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        if username:
            PlatformAccount.objects.update_or_create(
                user=request.user,
                platform=platform,
                defaults={
                    "username": username,
                    "profile_url": f"https://auth.geeksforgeeks.org/user/{username}/",
                }
            )
            stats, _ = UserStats.objects.get_or_create(user=request.user)
            stats.gfg_username = username
            stats.save(update_fields=["gfg_username"])
            return redirect("gfg_sync")

    return render(request, "core/add_gfg.html")


@login_required
def gfg_sync(request):
    try:
        from core.services.gfg import sync_gfg_by_username
        sync_gfg_by_username(request.user)
        messages.success(request, "GFG synced!")
    except Exception as e:
        messages.error(request, f"GFG sync failed: {e}")
    return redirect("profile")


@login_required
def disconnect_gfg(request):
    PlatformAccount.objects.filter(
        user=request.user, platform__slug="gfg"
    ).delete()
    stats, _ = UserStats.objects.get_or_create(user=request.user)
    stats.gfg_solved = 0
    stats.gfg_xp = 0
    stats.gfg_username = ""
    stats.save(update_fields=["gfg_solved", "gfg_xp", "gfg_username"])
    stats.recalculate_totals()
    messages.success(request, "GFG disconnected.")
    return redirect("profile")


# ==================================================
# CODECHEF
# ==================================================

@login_required
def add_codechef(request):
    platform, _ = Platform.objects.get_or_create(
        slug="codechef",
        defaults={"name": "CodeChef", "base_url": "https://www.codechef.com"}
    )

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        if username:
            PlatformAccount.objects.update_or_create(
                user=request.user,
                platform=platform,
                defaults={
                    "username": username,
                    "profile_url": f"https://www.codechef.com/users/{username}",
                }
            )
            stats, _ = UserStats.objects.get_or_create(user=request.user)
            stats.codechef_username = username
            stats.save(update_fields=["codechef_username"])
            return redirect("codechef_sync")

    return render(request, "core/add_codechef.html")


@login_required
def codechef_sync(request):
    try:
        from core.services.codechef import sync_codechef_by_username
        sync_codechef_by_username(request.user)
        messages.success(request, "CodeChef synced!")
    except Exception as e:
        messages.error(request, f"CodeChef sync failed: {e}")
    return redirect("profile")


@login_required
def disconnect_codechef(request):
    PlatformAccount.objects.filter(
        user=request.user, platform__slug="codechef"
    ).delete()
    stats, _ = UserStats.objects.get_or_create(user=request.user)
    stats.codechef_username = ""
    stats.codechef_solved = 0
    stats.codechef_rating = 0
    stats.codechef_contests = 0
    stats.codechef_xp = 0
    stats.save(update_fields=[
        "codechef_username",
        "codechef_solved",
        "codechef_rating",
        "codechef_contests",
        "codechef_xp",
    ])
    stats.recalculate_totals()
    messages.success(request, "CodeChef disconnected.")
    return redirect("profile")


# ==================================================
# HACKERRANK
# ==================================================

@login_required
def add_hackerrank(request):
    platform, _ = Platform.objects.get_or_create(
        slug="hackerrank",
        defaults={"name": "HackerRank", "base_url": "https://www.hackerrank.com"}
    )

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        if username:
            PlatformAccount.objects.update_or_create(
                user=request.user,
                platform=platform,
                defaults={
                    "username": username,
                    "profile_url": f"https://www.hackerrank.com/profile/{username}",
                }
            )
            stats, _ = UserStats.objects.get_or_create(user=request.user)
            stats.hackerrank_username = username
            stats.save(update_fields=["hackerrank_username"])
            return redirect("hackerrank_sync")

    return render(request, "core/add_hackerrank.html")


@login_required
def hackerrank_sync(request):
    try:
        from core.services.hackerrank import sync_hackerrank_by_username
        sync_hackerrank_by_username(request.user)
        messages.success(request, "HackerRank synced!")
    except Exception as e:
        messages.error(request, f"HackerRank sync failed: {e}")
    return redirect("profile")


@login_required
def disconnect_hackerrank(request):
    PlatformAccount.objects.filter(
        user=request.user, platform__slug="hackerrank"
    ).delete()
    stats, _ = UserStats.objects.get_or_create(user=request.user)
    stats.hackerrank_username = ""
    stats.hackerrank_solved = 0
    stats.hackerrank_xp = 0
    stats.save(update_fields=[
        "hackerrank_username",
        "hackerrank_solved",
        "hackerrank_xp",
    ])
    stats.recalculate_totals()
    messages.success(request, "HackerRank disconnected.")
    return redirect("profile")


# ==================================================
# STREAK ENGINE  (private helper — not a view)
# ==================================================

def _update_streak(user):
    """Update the user's study streak. Call after any study activity."""
    today = timezone.now().date()
    streak, _ = StudyStreak.objects.get_or_create(user=user)

    if streak.last_active == today:
        return  # already counted today
    elif streak.last_active == today - timezone.timedelta(days=1):
        streak.current_streak += 1
    else:
        streak.current_streak = 1  # streak broken

    streak.last_active = today
    streak.longest_streak = max(streak.longest_streak, streak.current_streak)
    streak.save()


# Keep old name as alias for backwards compatibility
update_streak = _update_streak


# ==================================================
# LEARNING GOALS
# ==================================================

@login_required
def learning_goals(request):
    goals = LearningGoal.objects.filter(user=request.user).order_by("-created_at")

    if request.method == "POST":
        form = LearningGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, "Goal added!")
            return redirect("learning_goals")
    else:
        form = LearningGoalForm()

    return render(request, "core/learning_goals.html", {
        "goals": goals,
        "form": form,
    })


@login_required
def start_learning(request, goal_id):
    """Generate learning path and resources for a goal."""
    goal = get_object_or_404(LearningGoal, id=goal_id, user=request.user)

    if not goal.ai_solution:
        try:
            goal.ai_solution = generate_goal_solution(goal.title)
            goal.save(update_fields=["ai_solution"])
        except Exception as e:
            logger.error(f"AI solution generation failed for goal {goal_id}: {str(e)}", exc_info=True)
            goal.ai_solution = "AI unavailable. Try again later."
            messages.warning(request, "Could not generate AI learning path. Please check your API configuration.")

    try:
        seed_resources_by_goal(goal.title)
    except Exception as e:
        logger.warning(f"Resource seeding failed for goal {goal_id}: {str(e)}")
        # Don't fail completely if resources can't be seeded

    # Get resources for this goal only
    resources = Resource.objects.filter(goal=goal).order_by("-id")[:12]

    return render(request, "core/start_learning.html", {
        "goal": goal,
        "solution": goal.ai_solution,
        "resources": resources,
    })


# ==================================================
# STUDY SESSIONS
# ==================================================

@login_required
def add_study_session(request):
    if request.method == "POST":
        form = StudySessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user
            session.study_date = timezone.now().date()
            session.save()
            _update_streak(request.user)
            messages.success(request, f"Study session of {session.duration_minutes} min logged!")
            return redirect("dashboard")
    else:
        form = StudySessionForm()

    return render(request, "core/add_study_session.html", {"form": form})


@login_required
def study_history(request):
    sessions = StudySession.objects.filter(
        user=request.user
    ).order_by("-study_date")

    total_minutes = sessions.aggregate(
        Sum("duration_minutes")
    )["duration_minutes__sum"] or 0

    return render(request, "core/study_history.html", {
        "sessions": sessions,
        "total_minutes": total_minutes,
        "total_hours": round(total_minutes / 60, 1),
    })


# ==================================================
# HEALTH CHECK (for deployment monitoring)
# ==================================================

@require_http_methods(["GET"])
def health_check(request):
    """
    Health check endpoint for monitoring.
    Returns JSON with status of key services.
    """
    try:
        # Check database connection
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        db_status = "ok"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "error"

    return JsonResponse({
        "status": "healthy" if db_status == "ok" else "degraded",
        "database": db_status,
        "timestamp": timezone.now().isoformat(),
    })


# ==================================================
# EDIT TASK
# ==================================================

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully!")
            return redirect("tasks_hub")
    else:
        form = TaskForm(instance=task)
    return render(request, "core/edit_task.html", {"form": form, "task": task})
