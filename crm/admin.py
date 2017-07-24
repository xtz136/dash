from django.contrib import admin
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import Company, People, ShareHolder, Contract
from core.models import Attachment


class AttachmentInline(GenericTabularInline):
    model = Attachment


class ShareHolderInline(admin.TabularInline):
    model = ShareHolder


class ContractInline(admin.TabularInline):
    model = Contract


@admin.register(Company)
class CompanyModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'view_expired_at', 'industry',
                    'taxpayer_type', 'scale_size', 'view_expired_at',
                    'has_expired',
                    'download')
    list_filter = ('type', 'salesman', 'industry',
                   'taxpayer_type', 'scale_size', 'status', 'has_expired')
    search_fields = ('title', )
    inlines = [
        ContractInline,
        ShareHolderInline,
        AttachmentInline
    ]

    def download(self, obj):
        return mark_safe('<a href="#">附件</a>')
    download.short_description = '下载附件'

    def view_expired_at(self, obj):
        return obj.expired_at
    view_expired_at.empty_value_display = '无期限'
    view_expired_at.short_description = '执照过期日期'


@admin.register(Contract)
class ContractModelAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    empty_value_display = '-空的-'
    actions_on_top = False
    actions_on_bottom = True
    list_filter = ('status', 'subscription_type')
    list_display = ('company_title', 'title', 'salesman_name',
                    'subscription_type', 'status', 'amount',
                    'receivables', 'received', 'view_arrearage',
                    'duration',
                    'created', 'expired_at')
    search_fields = ('company_title', 'salesmane_name')
    inlines = [
        AttachmentInline
    ]

    def view_arrearage(self, obj):
        if obj.arrearage > 0:
            return mark_safe('<span style="color:red">-{0}</span>'.format(obj.arrearage))
        return obj.arrearage
    view_arrearage.short_description = '欠款'


@admin.register(People)
class PeopleModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'sfz', 'phone')
    inlines = [
        AttachmentInline
    ]


@admin.register(ShareHolder)
class ShareHolderModelAdmin(admin.ModelAdmin):
    list_display = ('company_title', 'people_name', 'role', 'view_share')

    def view_share(self, obj):
        return '{:.2f}%'.format(obj.share * 100)
    view_share.short_description = '占比'
