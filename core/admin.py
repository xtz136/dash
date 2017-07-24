from django.contrib import admin

from .models import Attachment


admin.site.site_header = '来自远方的你'


@admin.register(Attachment)
class AttachmentModelAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', )
    list_filter = ('file_type', )
