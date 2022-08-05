from send_email.celery import app

from .models import User, Task


@app.task
def send_mail():
    for contact in User.objects.all():
        for content in Task.objects.all(user=contact.user):
            send_mail(
                [content.title, content.deadline]
                [contact.email],
                fail_silently=False,
            )
