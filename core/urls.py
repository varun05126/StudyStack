from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),

    path("dashboard/", views.dashboard, name="dashboard"),
    path("subjects/add/", views.add_subject, name="add_subject"),
    path("tasks/add/", views.add_task, name="add_task"),
]
