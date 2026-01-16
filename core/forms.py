from django import forms
from django.contrib.auth.models import User
from .models import Subject, Task

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password") != cleaned.get("confirm_password"):
            self.add_error("confirm_password", "Passwords do not match")
        return cleaned


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["name", "description"]


class TaskForm(forms.ModelForm):
    new_subject = forms.CharField(
        required=False,
        label="Or add new subject",
        widget=forms.TextInput(attrs={"placeholder": "Eg: Data Structures"})
    )

    class Meta:
        model = Task
        fields = ["title", "subject", "deadline", "estimated_hours", "difficulty"]
        widgets = {
            "deadline": forms.DateInput(attrs={"type": "date"}),
        }
