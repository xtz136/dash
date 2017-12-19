from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Follower(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    object_id = models.PositiveIntegerField(default=0)
    content_object = GenericForeignKey('content_type', 'object_id')
    content_type = models.ForeignKey(ContentType)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0} follow {1}'.format(self.user, self.content_object)
