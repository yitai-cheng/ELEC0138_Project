from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from datetime import timedelta
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myhomwwork.settings')
app = Celery('mysite')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'backup-every-day-at-4-34pm': {
        'task': 'mysite.tasks.backup_data_to_google_drive',
        'schedule': crontab(hour=16, minute=34),
        'args': (),
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
