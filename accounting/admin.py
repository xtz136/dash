from django.contrib import admin
from .models import *
from core.models import Attachment

from core.admin import AttachmentInline


@admin.register(Report)
class ReportModelAdmin(admin.ModelAdmin):
    list_display = ('company', 'bookkeeper', 'date', 'has_notified')
    list_filter = ('bookkeeper', 'has_notified')
    raw_id_fields = ('company', )
    search_fields = ('company__title', )
    date_hierarchy = 'date'
    inlines = [
        AttachmentInline
    ]

    actions = ('notify', )

    def notify(self, request, queryset):
        for obj in queryset:
            obj.send_message()

    notify.short_description = '微信通知'
