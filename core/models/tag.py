from django.db import models
from django.utils.timezone import now
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase


class Tag(TagBase):
    colour = models.CharField(max_length=255, blank=True)
    last_used = models.DateTimeField(default=now)

    def post_use(self):
        """最近一次使用标签"""
        self.last_used = now()
        self.save()

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'colour': self.colour
        }

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class TaggedItem(GenericTaggedItemBase):
    tag = models.ForeignKey(Tag,
                            related_name="%(app_label)s_%(class)s_items")
