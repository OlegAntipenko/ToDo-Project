from datetime import date
from django import forms
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    job_title = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Task(models.Model):
    title = models.CharField(max_length=150)
    text = models.TextField()
    status = models.CharField(
        choices=(
            ('todo', 'ToDo'),
            ('in_progres', 'In_progres'),
            ('blocked', 'Blocked'),
            ('finished', 'Finished')
        ),
        max_length=25,
        default='todo'
    )
    priorities = models.CharField(
        choices=(
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High')
        ),
        max_length=25,
        default='medium'
    )
    importance = models.BooleanField(default=False)
    deadline = models.DateField(default=date.today)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
