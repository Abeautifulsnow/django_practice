from __future__ import absolute_import, unicode_literals
from .celery import app as celery_app


# 给外部模块提供接口
__all__ = ['celery_app']
