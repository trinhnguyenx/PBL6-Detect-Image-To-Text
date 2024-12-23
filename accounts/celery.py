from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Đặt biến môi trường để chỉ định file cấu hình của Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'user_management.settings')

app = Celery('accounts')

# Đọc cấu hình Celery từ file settings.py của Django
app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks(lambda: ['accounts'])


