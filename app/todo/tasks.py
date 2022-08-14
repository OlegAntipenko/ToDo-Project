from datetime import date, timedelta
from django.core.mail import send_mail

from app.celery import app

from .models import User, Task


@app.task
def send_email():
    for user in User.objects.all():
        content = Task.objects.filter(user=user, deadline=date.today + timedelta(days=1)).values_list('title')
        send_mail(
            'Tasks expire:',
            content,
            [user.email],
        )


@app.task
def send_week_email():
    for user in User.objects.all():
        content = Task.objects.filter(user=user, status='finished',
                                      deadline=range(date.today - timedelta(days=6), date.today)).values_list('title')
        send_mail(
            'Completed in a week:',
            content,
            [user.email],
        )
