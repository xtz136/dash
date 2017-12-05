from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


from .models import WhiteList


@admin.register(WhiteList)
class WhiteListModelAdmin(admin.ModelAdmin):
    list_display = ('ip', 'domain')
    search_fields = ('ip', 'domain')
