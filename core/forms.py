from django import forms
from django.contrib.auth.models import User

from .models import (
    Subject,
    Topic,
    Task,
    Note,
    LearningGoal,
    StudySession,
)


# ================= AUTH =================

class SignupForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


# ================= SUBJECT =================

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. Data Structures"
            })
        }


# ================= NOTES =================

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "topic", "text_content", "file", "visibility"]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Note title"
            }),
            "topic": forms.Select(attrs={
                "class": "form-control"
            }),
            "text_content": forms.Textarea(attrs={
                "rows": 5,
                "class": "form-control",
                "placeholder": "Write your notes here..."
            }),
            "visibility": forms.Select(attrs={
                "class": "form-control"
            })
        }


# ================= TASK =================

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "title",
            "subject",
            "deadline",
            "estimated_hours",
            "completed",
        ]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. Complete Unit 3 Notes"
            }),
            "subject": forms.Select(attrs={
                "class": "form-control"
            }),
            "deadline": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),
            "estimated_hours": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.5",
                "placeholder": "e.g. 2.5"
            }),
        }


# ================= LEARNING GOALS =================

class LearningGoalForm(forms.ModelForm):
    class Meta:
        model = LearningGoal
        fields = ["title"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "What do you want to learn today?"
            })
        }


# ================= STUDY SESSION =================

class StudySessionForm(forms.ModelForm):
    class Meta:
        model = StudySession
        fields = ["topic", "duration_minutes"]

        widgets = {
            "topic": forms.Select(attrs={
                "class": "form-control"
            }),
            "duration_minutes": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Time in minutes (e.g. 45)"
            }),
        }
        