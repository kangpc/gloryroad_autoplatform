import os

from celery import Celery, platforms
# 获取settings.py的配置信息
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gloryroad_autoplatform.settings')
# 定义Celery对象，并将项目配置信息加载到对象中
# Celery的参数一般以项目名称命名
app = Celery('gloryroad_autoplatform')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
platforms.C_FORCE_ROOT = True