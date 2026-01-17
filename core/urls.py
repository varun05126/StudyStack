from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),   # default page = login
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),

    path("dashboard/", views.dashboard, name="dashboard"),

    path("add-task/", views.add_task, name="add_task"),
    path("complete/<int:task_id>/", views.mark_complete, name="mark_complete"),
    path("delete/<int:task_id>/", views.delete_task, name="delete_task"),

    path("subjects/", views.subjects, name="subjects"),
    path("delete-subject/<int:subject_id>/", views.delete_subject, name="delete_subject"),
]
