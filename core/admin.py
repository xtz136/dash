from django.contrib import admin
from solo.admin import SingletonModelAdmin


from .models import *


admin.site.site_header = '悦海财税'


@admin.register(Attachment)
class AttachmentModelAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', )
    list_filter = ('file_type', )


@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname')


@admin.register(Tag)
class TagModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'colour')


@admin.register(AccessToken)
class AccessTokenModelAdmin(admin.ModelAdmin):
    list_display = ('openid', 'user', 'created')


admin.site.register(SiteConf, SingletonModelAdmin)
