from django.contrib import admin

from .models import (
    LearningTrack,
    Subject,
    Topic,
    Resource,
    Problem,
    UserTopicProgress,
    Task,
    TaskMessage,
    Note,
    LearningGoal,
    StudySession,
    StudyStreak,
    Platform,
    PlatformAccount,
    DailyActivity,
    UserHeatmap,
    UserStats,
    LeaderboardEntry,
)

# ==================================================
#                ACADEMIC STRUCTURE
# ==================================================

@admin.register(LearningTrack)
class LearningTrackAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "track")
    list_filter = ("track",)
    search_fields = ("name", "track__name")


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "subject")
    list_filter = ("subject",)
    search_fields = ("name", "subject__name")


# ==================================================
#                RESOURCES & PRACTICE
# ==================================================

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "topic", "type", "is_best")
    list_filter = ("type", "is_best")
    search_fields = ("title",)
    list_editable = ("is_best",)


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ("title", "platform", "difficulty", "topic")
    list_filter = ("platform", "difficulty")
    search_fields = ("title", "platform")


@admin.register(UserTopicProgress)
class UserTopicProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "topic", "status", "mastery", "last_studied")
    list_filter = ("status",)
    search_fields = ("user__username", "topic__name")


# ==================================================
#                PRODUCTIVITY CORE
# ==================================================

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "task_type", "completed", "deadline")
    list_filter = ("task_type", "completed", "deadline")
    search_fields = ("title", "user__username")
    list_editable = ("completed",)
    date_hierarchy = "created_at"


@admin.register(TaskMessage)
class TaskMessageAdmin(admin.ModelAdmin):
    list_display = ("task", "sender", "created_at")
    list_filter = ("sender",)
    search_fields = ("task__title",)
    date_hierarchy = "created_at"


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "visibility", "created_at")
    list_filter = ("visibility", "created_at")
    search_fields = ("title", "text_content", "user__username")
    date_hierarchy = "created_at"


@admin.register(LearningGoal)
class LearningGoalAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "status", "is_satisfied", "created_at")
    list_filter = ("status", "is_satisfied")
    search_fields = ("title", "user__username")
    list_editable = ("status", "is_satisfied")


@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ("user", "topic", "duration_minutes", "study_date")
    list_filter = ("study_date",)
    search_fields = ("user__username",)
    date_hierarchy = "study_date"


@admin.register(StudyStreak)
class StudyStreakAdmin(admin.ModelAdmin):
    list_display = ("user", "current_streak", "longest_streak", "last_active")
    search_fields = ("user__username",)


# ==================================================
#                PLATFORM SYSTEM
# ==================================================

@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "slug")


@admin.register(PlatformAccount)
class PlatformAccountAdmin(admin.ModelAdmin):
    list_display = ("user", "platform", "username", "last_synced")
    search_fields = ("user__username", "username", "platform__name")
    list_filter = ("platform", "last_synced")


@admin.register(DailyActivity)
class DailyActivityAdmin(admin.ModelAdmin):
    list_display = ("account", "date", "xp")
    list_filter = ("date",)
    search_fields = ("account__user__username",)
    date_hierarchy = "date"


@admin.register(UserHeatmap)
class UserHeatmapAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "activity_score", "total_xp")
    list_filter = ("date",)
    search_fields = ("user__username",)
    date_hierarchy = "date"


# ==================================================
#                USER STATS / LEADERBOARD
# ==================================================

@admin.register(UserStats)
class UserStatsAdmin(admin.ModelAdmin):
    list_display = ("user", "total_xp", "level")
    search_fields = ("user__username",)


@admin.register(LeaderboardEntry)
class LeaderboardEntryAdmin(admin.ModelAdmin):
    list_display = ("rank", "user", "xp")
    ordering = ("rank",)
    search_fields = ("user__username",)
    readonly_fields = ("calculated_at",)