from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


def get_upload_to(instance, filename):
    return 'uploads/avatar/{id}/{filename}'.format(
        id=instance.id, filename=filename)


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mobile = models.CharField(verbose_name='手机', max_length=100, blank=True)
    avatar = models.ImageField(
        verbose_name='头像', blank=True, upload_to=get_upload_to)
    headimgurl = models.CharField(max_length=255, blank=True)
    nickname = models.CharField(max_length=200, blank=True)
    sex = models.SmallIntegerField(default=1, choices=((1, '男性'), (2, '女性'),))
    country = models.CharField('国家', max_length=50, default='中国')
    province = models.CharField('省', max_length=100, default='')
    city = models.CharField('城市', max_length=100, default='')
    prefs = JSONField(default={}, verbose_name='偏好设置', blank=True)


def save_profile(sender, instance, created, **kwargs):
    if not hasattr(instance, 'profile') or created:
        profile = Profile.objects.create(user=instance)


post_save.connect(save_profile, sender=User)
