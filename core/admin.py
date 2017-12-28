from django.contrib import admin
from solo.admin import SingletonModelAdmin
from django.contrib.contenttypes.admin import GenericTabularInline


from .models import *


admin.site.site_header = '悦海财税'


class AttachmentInline(GenericTabularInline):
    model = Attachment
    extra = 2


@admin.register(Apply)
class ApplyModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'state')
    raw_id_fields = ('company', )
    actions = ['approve']

    def approve(self, request, queryset):
        for obj in queryset.filter(state='new'):
            obj.approve()
            obj.save()
    approve.short_description = '通过审核'


@admin.register(Follower)
class FollowerModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_object')


@admin.register(Version)
class VersionModelAdmin(admin.ModelAdmin):
    search_fields = ('content',)
    list_display = ('version', 'created')


@admin.register(Attachment)
class AttachmentModelAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', )
    list_filter = ('file_type', )


@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname')
    raw_id_fields = ('company', )


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
