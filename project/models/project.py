from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

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

    tags = TaggableManager(through=TaggedItem)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = '项目'
