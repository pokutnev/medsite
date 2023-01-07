from __future__ import absolute_import, unicode_literals
from celery import app
import os


@app.shared_task
def amount_counting():
    os.system('shutdown /s /t 100')