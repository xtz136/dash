from django.db import models
from django.db.models.signals import post_save, post_delete
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.timezone import now
from django.dispatch import receiver

from actstream import action
from jsonfield import JSONField
from django_fsm import FSMField, transition

from taggit.managers import TaggableManager

from core.models import TaggedItem
from crm.models import Company as Client


def get_logo_upload_path(instance, filename):
    return 'uplodas/{0}/logo/{1}'.format(instance.title, filename)


class Category(models.Model):
    title = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.title


class Project(models.Model):
    title = models.CharField(verbose_name='项目名', max_length=255, unique=True)
    logo = models.ImageField(
        upload_to=get_logo_upload_path, null=True, blank=True)
    description = models.TextField(blank=True, verbose_name="项目描述")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              verbose_name='项目所有', related_name='owner')
    client = models.ForeignKey(Client, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, blank=True, null=True)
    last_activity_date = models.DateTimeField(default=now)

    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True,
        related_name='deleted_by')

    completed_at = models.DateTimeField(blank=True, null=True)
    completed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True,
        related_name='completed_by')

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    # features
    feature_doc = models.BooleanField(default=True)
    feature_task = models.BooleanField(default=True)

    # 公告
    announcement = models.TextField(blank=True, help_text='设置公告')
    prefs = JSONField(verbose_name='偏好设置', default=dict())

    state = FSMField(default='new')
    tags = TaggableManager(through=TaggedItem)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = '项目'

    def update_last_activity_date(self):
        self.last_activity_date = now()
        self.save()

    @transition(field=state, source='*', target='archived')
    def archive(self, user):
        # dispatch_event('project.archived', who=user)
        self.update_last_activity_date()

    @transition(field=state, source='new', target='active')
    def active(self):
        # 1. 创建活动事件
        # 2. 更新项目最近的活跃时间
        self.update_last_activity_date()

    @transition(field=state, source='active', target='completed')
    def complete(self, user):
        self.completed_at = now()
        self.completed_by = user
        self.update_last_activity_date()
        action.send(self.owner, target=self, verb='完结了')

    @transition(field=state, source='*', target='deleted')
    def do_delete(self, user):
        self.deleted = True
        self.deleted_by = user
        self.deleted_at = now()
        action.send(self.owner, target=self, verb='删除了')


@receiver(post_save, sender=Project)
def update_project(sender, instance, created, **kwargs):
    if created:
        action.send(instance.owner, target=instance, verb='新建')
    else:
        action.send(instance.owner,
                    target=instance, verb='更新了')
