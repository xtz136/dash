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


@admin.register(MemberApplication)
class MemberApplicationModelAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'company_title', 'state', 'created')
    list_filter = ('state',)
    actions = ('approved', 'denied')

    def approved(self, request, queryset):
        for obj in queryset:
            obj.approved()

    def denied(self, request, queryset):
        for obj in queryset:
            obj.denied()


admin.site.register(SiteConf, SingletonModelAdmin)
