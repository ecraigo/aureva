# Celery server for Aureva; run asynchronous tasks on server that vanilla Python cannot do alone
from __future__ import absolute_import
import os
from celery import Celery

# Set Celery's default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Aureva.settings')

from django.conf import settings

app = Celery('Aureva', backend='amqp', broker='amqp://')

# We don't need to use multiple config files, thanks to these lines of code
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)