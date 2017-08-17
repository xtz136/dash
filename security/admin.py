from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


from .models import WhiteList, Profile


@admin.register(WhiteList)
class WhiteListModelAdmin(admin.ModelAdmin):
    list_display = ('ip', 'domain')
    search_fields = ('ip', 'domain')


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = '职员'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
