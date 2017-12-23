from django.contrib import admin
from .models import *
from core.models import Attachment

from core.admin import AttachmentInline


@admin.register(Report)
class ReportModelAdmin(admin.ModelAdmin):
    list_display = ('company', 'bookkeeper', 'date')
    list_filter = ('bookkeeper', )
    raw_id_fields = ('company', )
    search_fields = ('company__title', )
    date_hierarchy = 'date'
    inlines = [
        AttachmentInline
    ]
