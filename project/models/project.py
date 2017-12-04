from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.timezone import now

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
                              verbose_name='项目所有者', related_name='owner')
    client = models.ForeignKey(Client, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, blank=True, null=True)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='members', blank=True)

    last_activity_date = models.DateTimeField(default=now)
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True)

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    # features
    feature_doc = models.BooleanField(default=True)
    feature_task = models.BooleanField(default=True)

    prefs = JSONField(verbose_name='偏好设置', default=dict())

    state = FSMField(default='new')
    tags = TaggableManager(through=TaggedItem)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = '项目'

    @transition(field=state, source='*', target='archived')
    def archive(self, user):
        pass
        # dispatch_event('project.archived', who=user)

    @transition(field=state, source='new', target='active')
    def active(self):
        pass
        # dispatch_event('project.new', who=self.owner)

    @transition(field=state, source='*', target='deleted')
    def do_delete(self, user):
        self.deleted = True
        self.deleted_by = user
        self.deleted_at = now()
        self.save()
        # dispatch_event('project.delete', who=user)
