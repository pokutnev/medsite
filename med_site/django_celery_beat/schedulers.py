from django.core.management import call_command
from celery import Celery
from celery.schedules import crontab

app = Celery()

@app.task
def DatabaseScheduler():
    try:
        call_command('dbbackup')
    except:
        pass