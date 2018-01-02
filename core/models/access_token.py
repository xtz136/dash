from datetime import timedelta
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from django.conf import settings

from wechatpy.oauth import WeChatOAuth


class AccessToken(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, blank=True, null=True,
        related_name='access_token')
    openid = models.CharField(max_length=255, unique=True)
    access_token = models.CharField(max_length=255, blank=True)
    refresh_token = models.CharField(max_length=255, blank=True)
    expires_in = models.IntegerField(default=0)
    scope = models.CharField(max_length=200, default='snsapi_userinfo')
    created = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now_add=True)

    def has_expired(self):
        return now() - self.last_updated_at >= timedelta(seconds=self.expires_in)

    def refresh(self):
        client = WeChatOAuth(settings.WX_APPID,
                             settings.WX_APPSECRET,
                             settings.WX_REDIRECT_URI,
                             scope=self.scope)
        token = client.refresh_token(self.refresh_token)
        self.refresh_token = token['refresh_token']
        self.access_token = token['access_token']
        self.expires_in = token['expires_in']
        self.scope = token['scope']
        self.save()

    def update_token(self,
                     access_token,
                     fields=['access_token', 'refresh_token',
                             'expires_in', 'scope']
                     ):
        for field in fields:
            if field in access_token:
                setattr(self, field, access_token[field])
        self.last_updated_at = now()
        self.save()

    def __str__(self):
        return 'AccessToken <{0}>'.format(self.user)
