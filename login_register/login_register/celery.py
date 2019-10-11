from __future__ import absolute_import, unicode_literals

import os
from celery import Celery
from django.conf import settings


# 获取当前文件的上层目录名称
proj_name = os.path.split(os.path.abspath('.'))[-1]
print(proj_name)
proj_settings = f"{proj_name}.settings"
print(proj_settings)
# 设置环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE", proj_settings)

# 实例化celery
app = Celery(proj_name)
# 读取配置文件
app.config_from_object("django.conf:settings", namespace="CELERY")
# 自动发现tasks任务
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
