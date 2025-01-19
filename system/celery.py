# src/project_name/celery.py
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'system.settings')

app = Celery('system')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-patient-details-every-day': {
        'task': 'patients.tasks.send_all_patients_email',
        'schedule': crontab(hour=14, minute=20),
    },
}