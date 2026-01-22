from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL

# ================= LEARNING TRACK =================
# Example: DSA, Web Development, AI/ML, Core CS

class LearningTrack(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# ================= SUBJECT =================
# Example: DSA → Arrays, Web → Django, AI → ML Basics

class Subject(models.Model):
    track = models.ForeignKey(LearningTrack, on_delete=models.CASCADE, related_name="subjects")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.track.name} - {self.name}"


# ================= TOPIC =================
# Example: Arrays → Two Pointers, Django → Authentication

class Topic(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="topics")
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.subject.name} - {self.name}"


# ================= RESOURCE =================

class Resource(models.Model):
    RESOURCE_TYPES = [
        ("video", "Video"),
        ("article", "Article"),
        ("course", "Course"),
        ("book", "Book"),
        ("docs", "Documentation"),
    ]

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="resources")
    title = models.CharField(max_length=200)
    url = models.URLField()
    type = models.CharField(max_length=12, choices=RESOURCE_TYPES)
    is_best = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.type})"


# ================= PROBLEM =================

class Problem(models.Model):
    DIFFICULTY = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="problems")
    title = models.CharField(max_length=200)
    platform = models.CharField(max_length=50)  # LeetCode, GFG, CF, HackerRank
    url = models.URLField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY)

    def __str__(self):
        return f"{self.title} - {self.platform}"


# ================= USER TOPIC PROGRESS =================

class UserTopicProgress(models.Model):
    STATUS = [
        ("not_started", "Not Started"),
        ("learning", "Learning"),
        ("completed", "Completed"),
        ("revising", "Revising"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=STATUS, default="not_started")
    mastery = models.PositiveIntegerField(default=0)  # 0–100
    last_studied = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "topic")

    def __str__(self):
        return f"{self.user} - {self.topic} ({self.status})"


# ================= TASK =================

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    deadline = models.DateField()
    estimated_hours = models.DecimalField(max_digits=4, decimal_places=1)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ================= NOTE =================

class Note(models.Model):
    VISIBILITY = [("private", "Private"), ("public", "Public")]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    text_content = models.TextField(blank=True)
    file = models.FileField(upload_to="notes/", blank=True, null=True)
    visibility = models.CharField(max_length=10, choices=VISIBILITY, default="private")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ================= LEARNING GOAL =================

class LearningGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ================= STUDY SESSION =================

class StudySession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)
    duration_minutes = models.PositiveIntegerField()
    study_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user} - {self.duration_minutes} min"


# ================= STUDY STREAK =================

class StudyStreak(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    last_active = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.current_streak}"