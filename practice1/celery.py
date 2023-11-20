from __future__ import absolute_import,unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "practice1.settings")
app = Celery("practice1")

app.conf.enable_utc=False
app.conf.update(timezone='Asia/Ho_Chi_Minh')

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
    
#celery beat settings
app.conf.beat_schedule={
    'send-mail-every-minute':{
        'task':'worker.tasks.send_mail_to_admins_func',
        'schedule': crontab(),
    },
    'health-check-every-minute':{
        'task':'worker.tasks.health_check_per_minute',
        'schedule': crontab(),
    }
}