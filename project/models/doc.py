import os.path
from django.db import models
from mimetypes import guess_extension
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

from mptt.models import MPTTModel, TreeForeignKey

from .project import Project
from crm.models import Company as Client


class Folder(MPTTModel):
    name = models.CharField(max_length=200)
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children', db_index=True)
    project = models.ForeignKey(Project)

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']
        verbose_name = '文件夹'
        verbose_name_plural = '文件夹'


def get_upload_path(instance, filename):
    return 'uploads/projects/{0}/{1}/{2}'.format(
        instance.project or 'tmp', now().strftime('%Y/%m/%d'),
        filename)


class File(models.Model):
    """文档模型"""
    name = models.CharField(max_length=255,
                            verbose_name="文件名", blank=True)
    file = models.FileField(upload_to=get_upload_path)
    description = models.TextField(blank=True)
    folder = models.ForeignKey(
        Folder, verbose_name='文件夹', null=True, blank=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='创建人', blank=True, null=True)
    status = models.CharField(max_length=50, default='normal', choices=(
        ('active', '可见'),
        ('delete', '删除'),
    ))
    file_type = models.CharField(max_length=200, editable=False, blank=True)
    ext = models.CharField(max_length=200, editable=False, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # 锁定
    locked = models.BooleanField(default=False)
    locked_at = models.DateTimeField(blank=True, null=True)
    locked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, related_name='locked_by')

    # 文档所属项目
    project = models.ForeignKey(Project, null=True, blank=True)

    # 关联的泛型模型, 可以是评论附件，任务附件
    object_id = models.PositiveIntegerField(default=0)
    content_object = GenericForeignKey('content_type', 'object_id')
    content_type = models.ForeignKey(ContentType, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.file_type = self.file.file.content_type
        self.ext = os.path.splitext(self.file.file.name)[1]
        if not self.name:
            self.name = self.file.file.name
        return super(File, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '文档'
        verbose_name_plural = '文档'


class ShareLink(models.Model):
    file = models.ForeignKey(File)
    link = models.UUIDField(unique=True)
    expire = models.DateTimeField(blank=True, null=False)
    password = models.CharField(blank=True, max_length=50)
    once = models.BooleanField(default=False)

    def is_valid(self):
        if self.expire and self.expire <= now():
            return False
        return True

    def check_password(self, password):
        return self.password == password
