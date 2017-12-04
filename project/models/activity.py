from django.db import models
from django.conf import settings

from jsonfield import JSONField

from .project import Project
from django.contrib.auth.models import User


class Activity(models.Model):
    """事件的组成： 时间+地点+人物+内容"""
    who = models.ForeignKey(settings.AUTH_USER_MODEL)
    kind = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    content = JSONField(default=dict())
    project = models.ForeignKey(Project)
