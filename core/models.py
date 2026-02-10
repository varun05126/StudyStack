from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL


# ==================================================
#                ACADEMIC STRUCTURE
# ==================================================

class LearningTrack(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Subject(models.Model):
    track = models.ForeignKey("LearningTrack", on_delete=models.CASCADE, related_name="subjects")
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ("track", "name")
        ordering = ["name"]

    def __str__(self):
        return f"{self.track.name} - {self.name}"


class Topic(models.Model):
    subject = models.ForeignKey("Subject", on_delete=models.CASCADE, related_name="topics")
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ("subject", "name")
        ordering = ["name"]

    def __str__(self):
        return f"{self.subject.name} - {self.name}"


class LearningGoal(models.Model):
    STATUS = [
        ("planned", "Planned"),
        ("learning", "Learning"),
        ("completed", "Completed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="goals")
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=15, choices=STATUS, default="planned")

    ai_solution = models.TextField(blank=True)
    is_satisfied = models.BooleanField(null=True, blank=True)
    satisfaction_note = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title


# ==================================================
#                     NOTES
# ==================================================

class Note(models.Model):

    VISIBILITY = [
        ("private", "Private"),
        ("public", "Public"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    title = models.CharField(max_length=200)
    text_content = models.TextField(blank=True)

    visibility = models.CharField(
        max_length=10,
        choices=VISIBILITY,
        default="private"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ==================================================
#                RESOURCES & PRACTICE
# ==================================================

class Resource(models.Model):
    topic = models.ForeignKey("Topic", on_delete=models.CASCADE, related_name="resources")
    title = models.CharField(max_length=255)
    url = models.URLField()
    type = models.CharField(max_length=15)
    is_best = models.BooleanField(default=False)
    short_description = models.TextField(blank=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Problem(models.Model):
    topic = models.ForeignKey("Topic", on_delete=models.CASCADE, related_name="problems")
    title = models.CharField(max_length=200)
    platform = models.CharField(max_length=50)
    url = models.URLField()
    difficulty = models.CharField(max_length=10)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} ({self.platform})"


# ==================================================
#                STUDY ENGINE
# ==================================================

class StudySession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="study_sessions")
    topic = models.ForeignKey("Topic", on_delete=models.SET_NULL, null=True, blank=True)
    duration_minutes = models.PositiveIntegerField()
    study_date = models.DateField(default=timezone.now)

    class Meta:
        ordering = ["-study_date"]

    def __str__(self):
        return f"{self.user} - {self.duration_minutes} min"


class StudyStreak(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="study_streak")
    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    last_active = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.current_streak} days"


class UserTopicProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="topic_progress")
    topic = models.ForeignKey("Topic", on_delete=models.CASCADE)

    status = models.CharField(max_length=15, default="not_started")
    mastery = models.PositiveIntegerField(default=0)
    last_studied = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "topic")
        ordering = ["-last_studied"]

    def __str__(self):
        return f"{self.user} - {self.topic}"


# ==================================================
#                PRODUCTIVITY CORE
# ==================================================

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    subject = models.ForeignKey("Subject", on_delete=models.SET_NULL, null=True, blank=True)
    custom_subject = models.CharField(max_length=150, blank=True)

    material = models.FileField(upload_to="tasks/", blank=True, null=True)
    deadline = models.DateField(null=True, blank=True)
    estimated_hours = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)

    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    TASK_TYPES = [
    ("assignment", "Assignment"),
    ("study", "Study"),
    ("revision", "Revision"),
    ("project", "Project"),
    ("exam", "Exam"),
    ("reading", "Reading"),
    ("other", "Other"),
]

    task_type = models.CharField(
    max_length=20,
    choices=TASK_TYPES,
    default="study"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class TaskMessage(models.Model):
    task = models.ForeignKey("Task", on_delete=models.CASCADE, related_name="messages")
    sender = models.CharField(max_length=10)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]


# ==================================================
#           MULTI-PLATFORM ACTIVITY ENGINE
# ==================================================

class Platform(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class PlatformAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="platform_accounts")
    platform = models.ForeignKey("Platform", on_delete=models.CASCADE)
    username = models.CharField(max_length=150)
    last_synced = models.DateTimeField(null=True, blank=True)


class DailyActivity(models.Model):
    account = models.ForeignKey("PlatformAccount", on_delete=models.CASCADE)
    date = models.DateField()
    xp = models.PositiveIntegerField(default=0)

class UserHeatmap(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="heatmap"
    )
    date = models.DateField()

    total_xp = models.PositiveIntegerField(default=0)
    activity_score = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("user", "date")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.user} - {self.date}"
    

# ==================================================
#                USER STATS
# ==================================================

class UserStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="stats")

    github_username = models.CharField(max_length=150, blank=True, null=True)
    leetcode_username = models.CharField(max_length=150, blank=True, null=True)
    gfg_username = models.CharField(max_length=150, blank=True, null=True)
    codeforces_username = models.CharField(max_length=150, blank=True, null=True)
    hackerrank_username = models.CharField(max_length=150, blank=True, null=True)

    github_repos = models.PositiveIntegerField(default=0)   # ✅ REQUIRED

    total_commits = models.PositiveIntegerField(default=0)
    github_xp = models.PositiveIntegerField(default=0)

    leetcode_solved = models.PositiveIntegerField(default=0)
    leetcode_easy = models.PositiveIntegerField(default=0)
    leetcode_medium = models.PositiveIntegerField(default=0)
    leetcode_hard = models.PositiveIntegerField(default=0)
    leetcode_xp = models.PositiveIntegerField(default=0)

    gfg_solved = models.PositiveIntegerField(default=0)
    gfg_xp = models.PositiveIntegerField(default=0)

    codeforces_solved = models.PositiveIntegerField(default=0)
    codeforces_xp = models.PositiveIntegerField(default=0)

    hackerrank_solved = models.PositiveIntegerField(default=0)
    hackerrank_xp = models.PositiveIntegerField(default=0)

    total_xp = models.PositiveIntegerField(default=0)
    total_problems = models.PositiveIntegerField(default=0)
    total_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)

    last_updated = models.DateTimeField(auto_now=True)

    def recalculate_totals(self):
        self.total_xp = (
            self.github_xp
            + self.leetcode_xp
            + self.gfg_xp
            + self.codeforces_xp
            + self.hackerrank_xp
        )
        self.level = max(1, self.total_xp // 100)
        self.save(update_fields=["total_xp", "level"])

    def __str__(self):
        return f"{self.user} - {self.total_xp} XP"


class LeaderboardEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    xp = models.PositiveIntegerField()
    rank = models.PositiveIntegerField()
