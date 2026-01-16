from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subjects")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    DIFFICULTY_CHOICES = [
        (1, "Very Easy"),
        (2, "Easy"),
        (3, "Medium"),
        (4, "Hard"),
        (5, "Very Hard"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="tasks")

    title = models.CharField(max_length=200)
    deadline = models.DateField()
    estimated_hours = models.DecimalField(max_digits=4, decimal_places=1)
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
