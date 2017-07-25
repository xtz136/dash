from django.contrib import admin
from django.db import models
from django.forms import Textarea
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils import timezone

from .models import Company, People, ShareHolder, Contract, TaxBureau
from core.models import Attachment


class AttachmentInline(GenericTabularInline):
    model = Attachment
    extra = 2


class ShareHolderInline(admin.TabularInline):
    model = ShareHolder
    raw_id_fields = ('people', )
    extra = 1
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 40})}
    }


class ContractInline(admin.TabularInline):
    model = Contract


class HasExpiredFilter(admin.SimpleListFilter):
    title = '是否过期'
    parameter_name = 'has_expired'

    def lookups(self, request, model_admin):
        return (
            ('expired', '已过期'),
            ('not_expire', '未过期'),
        )

    def queryset(self, request, queryset):

        if self.value() == 'expired':
            return queryset.filter(expired_at__lte=timezone.now())
        elif self.value() == 'not_expire':
            return queryset.filter(
                Q(expired_at__gt=timezone.now()) | Q(expired_at=None))
        return queryset


@admin.register(Company)
class CompanyModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'industry',
                    'salesman', 'bookkeeper',
                    'taxpayer_type', 'scale_size', 'view_expired_at',
                    'status', 'download')
    list_filter = ('type', 'salesman', 'industry',
                   HasExpiredFilter,
                   'taxpayer_type', 'scale_size', 'status')
    search_fields = ('title', 'note', 'address', 'op_address')
    inlines = [
        # ContractInline,
        ShareHolderInline,
        AttachmentInline
    ]
    raw_id_fields = ('national_tax_office', 'local_tax_office')

    fieldsets = (
        ('公司信息', {
            'fields': ('title', 'type', 'registered_capital',
                       'industry', 'taxpayer_type', 'scale_size',
                       'credit_rating',
                       'address', 'op_address',
                       'uscc', 'business_license',
                       'website', 'salesman', 'bookkeeper',
                       'registered_at', 'expired_at',
                       'status', 'note')
        }),
        ('银行信息', {
            'fields': (
                ('ss_number', 'ss_date'),
                ('taxpayer_bank', 'taxpayer_account'),
                ('ss_bank', 'ss_account'),
                ('individual_bank', 'individual_account')
            )
        }),
        ('国税', {
            # 'classes': ('collapse',),
            'fields': (
                'national_tax_office',
                'national_tax_id',
                'national_tax_sn',
                'national_tax_staff',
                'national_tax_phone')
        }),
        ('地税', {
            'fields': (
                'local_tax_office',
                'local_tax_id',
                'local_tax_sn',
                'local_tax_staff',
                'local_tax_phone')
        }),
        ('海关信息', {
            'fields': (
                'custom_entry_no',
                'custom_org_code',
                'custom_register_no',
                'custom_registered_at',
                'custom_expired_at',
                'premise',
            )
        }),
    )

    def download(self, obj):
        return mark_safe('<a href="#">附件</a>')
    download.short_description = '下载'

    def view_expired_at(self, obj):
        return obj.expired_at
    view_expired_at.empty_value_display = '永久有效'
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
            return mark_safe('<span style="color:red">-{0}</span>'
                             .format(obj.arrearage))
        return obj.arrearage
    view_arrearage.short_description = '欠款'


@admin.register(People)
class PeopleModelAdmin(admin.ModelAdmin):
    search_fields = ('name', 'sfz', 'phone')
    list_display = ('name', 'sfz', 'phone')
    inlines = [
        AttachmentInline
    ]


@admin.register(ShareHolder)
class ShareHolderModelAdmin(admin.ModelAdmin):
    search_fields = ('company_title', 'people_name', 'info')
    list_display = ('company_title', 'people_name',
                    'phone', 'role', 'view_share', 'is_contactor')
    raw_id_fields = ('people', 'company')
    list_filter = ('is_contactor', )

    def view_share(self, obj):
        return '{:.2f}%'.format(obj.share)
    view_share.short_description = '占比'


@admin.register(TaxBureau)
class TaxBureauModelAdmin(admin.ModelAdmin):
    search_fields = ('office', 'address')
    list_filter = ('district', 'bureau')
    list_display = ('office', 'district', 'address', 'view_map')

    def view_map(self, obj):
        return mark_safe(
            "<a href='http://api.map.baidu.com/geocoder?address={0}{1}&output=html' target='_blank'>查看地图</a>".format(
                obj.get_district_display(), obj.office))
    view_map.short_description = '查看地图信息'
