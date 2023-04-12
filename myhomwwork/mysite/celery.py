from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from datetime import timedelta
from django_redis import get_redis_connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myhomwwork.settings')
app = Celery('mysite')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

redis_conn = get_redis_connection()

app.conf.beat_schedule = {
    'backup-every-day-at-6-10pm': {
        'task': 'mysite.task.backup_data_to_google_drive',
        'schedule': timedelta(hours=18, minutes=10),
        'args': (),
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')