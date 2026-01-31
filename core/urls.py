from django.urls import path
from . import views

urlpatterns = [

    # ================= AUTH =================
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),

    # ================= DASHBOARD =================
    path("", views.dashboard, name="dashboard"),
    path("dashboard/", views.dashboard, name="dashboard"),

    # ================= TASKS =================
    path("tasks/", views.tasks_hub, name="tasks_hub"),
    path("task/toggle/<int:task_id>/", views.toggle_task, name="toggle_task"),

    # ✅ Task detail + AI chat (single powerful route)
    path("tasks/<int:task_id>/", views.task_detail, name="task_detail"),
    path("tasks/<int:task_id>/need-help/", views.task_need_help, name="task_need_help"),

    # ================= NOTES =================
    path("notes/add/", views.add_note, name="add_note"),
    path("notes/my/", views.my_notes, name="my_notes"),
    path("notes/library/", views.public_library, name="public_library"),

    # ================= LEARNING GOALS =================
    path("goals/", views.learning_goals, name="learning_goals"),
    path("goals/<int:goal_id>/start/", views.start_learning, name="start_learning"),

    # ================= STUDY =================
    path("study/add/", views.add_study_session, name="add_study_session"),
    path("study/history/", views.study_history, name="study_history"),

    # ================= PROFILE =================
    path("profile/", views.profile, name="profile"),

    # ================= GITHUB =================
    path("github/add/", views.add_github_username, name="add_github"),
    path("github/sync/", views.sync_github, name="github_sync"),
    path("github/disconnect/", views.disconnect_github, name="disconnect_github"),
    path("github/activity/", views.github_activity, name="github_activity"),

    # ================= LEETCODE =================
    path("leetcode/add/", views.add_leetcode, name="add_leetcode"),
    path("leetcode/sync/", views.leetcode_sync, name="leetcode_sync"),
    path("leetcode/disconnect/", views.disconnect_leetcode, name="disconnect_leetcode"),

    # ---------- GFG ----------
    path("gfg/add/", views.add_gfg, name="add_gfg"),
    path("gfg/sync/", views.gfg_sync, name="gfg_sync"),
    path("gfg/disconnect/", views.disconnect_gfg, name="disconnect_gfg"),

# ---------- CODEFORCES ----------
    # path("codeforces/add/", views.add_codeforces, name="add_codeforces"),
    # path("codeforces/sync/", views.codeforces_sync, name="codeforces_sync"),
    # path("codeforces/disconnect/", views.disconnect_codeforces, name="disconnect_codeforces"),

# ---------- HACKERRANK ----------
    # path("hackerrank/add/", views.add_hackerrank, name="add_hackerrank"),
    # path("hackerrank/sync/", views.hackerrank_sync, name="hackerrank_sync"),
    # path("hackerrank/disconnect/", views.disconnect_hackerrank, name="disconnect_hackerrank"),
]
