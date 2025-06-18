# auth_project/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather.settings')

# Create Celery app
app = Celery('weather')

# Use a string here to make sure the worker doesn't serialize the object
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks from all registered Django apps (provide the correct path to the app)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Optional: Add a debug task to verify configuration
@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
