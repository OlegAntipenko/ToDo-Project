import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-regularly-mail': {
        'task': 'app.tasks.send_mail',
        'schedule': crontab(minute=0, hour=8),
    }
}

app.conf.beat_schedule = {
    'send-regularly-mail': {
        'task': 'app.tasks.send_week_email',
        'schedule': crontab(minute=0, hour=8, day_of_week='sat'),
    }
}
