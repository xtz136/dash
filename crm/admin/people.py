from django.contrib import admin
from crm.models import People
from .common import AttachmentInline


@admin.register(People)
class PeopleModelAdmin(admin.ModelAdmin):
    search_fields = ('name', 'sfz', 'phone')
    list_display = ('name', 'sfz', 'phone')
    inlines = [
        AttachmentInline
    ]
