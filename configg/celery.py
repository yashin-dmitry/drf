from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Установите переменную окружения для настройки Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configg.settings')

app = Celery('configg')

# Используйте строку для настройки Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически загружайте задачи из всех установленных приложений
app.autodiscover_tasks()
