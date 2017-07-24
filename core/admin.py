from django.contrib import admin

from .models import Attachment


admin.site.site_header = '悦海财税'


@admin.register(Attachment)
class AttachmentModelAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', )
    list_filter = ('file_type', )
