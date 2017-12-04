from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

from .project import Project


class Member(models.Model):
    project = models.ForeignKey(Project)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    role = models.CharField(default='member', max_length=50, choices=(
        ('owner', '创建人'),
        ('follower', '关注者'),
        ('member', '成员'),
    ))
    permissions = models.CharField(blank=True, max_length=255)


class Group(models.Model):
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project)
    members = models.ManyToManyField(Member)

    class Meta:
        unique_together = ('name', 'project')
