from datetime import date

from app.celery import app

from .models import User, Task


@app.task
def send_mail():
    for contact in User.objects.all():
        for content in Task.objects.all(user=contact.user).filter(deadline=date.today + 1):
            send_mail(
                'Tasks expire:',
                [content.title],
                [contact.email],
                fail_silently=False,
            )
