from django.contrib.auth.models import User
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.utils import timezone
from datetime import timedelta

from core.models import Attachment


class People(models.Model):
    name = models.CharField(name="企业名称",  max_length=255)
    sfz = models.CharField(name="身份证",  max_length=255, unique=True)

    GENDERS = (("male", "男性"), ("female", "女性"))
    gender = models.CharField(
        name="性别", choices=GENDERS, default="male", max_length=5)

    birthdate = models.DateField(name="生日", blank=True)
    phone = models.CharField(name="电话", blank=True, max_length=100)

    # 社交账号
    wechat = models.CharField(name="微信", blank=True, max_length=100)
    weibo = models.CharField(name="微博", blank=True, max_length=100)
    qq = models.CharField(name="QQ", blank=True, max_length=100)

    note = models.TextField(name="备注", blank=True)

    def __str__(self):
        return self.name

    @property
    def age(self):
        if self.birthdate:
            return (timezone.now() - self.birthdate) // timedelta(days=365.2425)
        return 0
