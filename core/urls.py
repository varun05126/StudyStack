from django.urls import path
from . import views

urlpatterns = [
    # -------- Auth --------
    path("", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),

    # -------- Dashboard & Tasks --------
    path("profile/", views.profile, name="profile"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("add-task/", views.add_task, name="add_task"),
    path("tasks/", views.my_tasks, name="my_tasks"),
    path("task/toggle/<int:task_id>/", views.toggle_task, name="toggle_task"),

    # -------- Notes --------
    path("notes/add/", views.add_note, name="add_note"),
    path("notes/my/", views.my_notes, name="my_notes"),
    path("notes/library/", views.public_library, name="public_library"),

    # -------- Learning Goals --------
    path("goals/", views.learning_goals, name="learning_goals"),

    # -------- Study Sessions --------
    path("study/add/", views.add_study_session, name="add_study_session"),
    path("study/history/", views.study_history, name="study_history"),

    # ------- GitHub Integration --------
    path("platforms/github/connect/", views.github_connect, name="github_connect"),
    path("platforms/github/callback/", views.github_callback, name="github_callback"),
    path("sync/github/", views.sync_github, name="sync_github"),
]