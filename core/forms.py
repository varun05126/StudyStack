from django import forms
from django.contrib.auth.models import User
from .models import Subject, Task


# ---------- AUTH FORM ----------

class SignupForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Username"
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Email address"
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Password"
    }))


# ---------- SUBJECT FORM ----------

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. Data Structures"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Optional description",
                "rows": 3
            }),
        }


# ---------- TASK FORM ----------

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "subject", "deadline", "estimated_hours", "difficulty"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. Complete Unit 3 Notes"
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
            "difficulty": forms.Select(attrs={
                "class": "form-control"
            }),
            "subject": forms.Select(attrs={
                "class": "form-control"
            }),
        }
