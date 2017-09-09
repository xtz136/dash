from django.contrib.contenttypes.admin import GenericTabularInline
from core.models import Attachment


class AttachmentInline(GenericTabularInline):
    model = Attachment
    extra = 2
