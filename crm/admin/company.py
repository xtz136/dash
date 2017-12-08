from django.contrib import admin
from django.db import models
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.shortcuts import redirect
from ajax_select import make_ajax_form

from admin_view_permission.admin import AdminViewPermissionModelAdmin

from crm.models import Company, ShareHolder, Contract, TaxBureau
from crm.actions import export_as_csv_action
from .shareholder import ShareHolderInline

from .common import AttachmentInline


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
class CompanyModelAdmin(AdminViewPermissionModelAdmin):
    list_display = ('title', 'industry',
                    'salesman', 'bookkeeper',
                    'taxpayer_type', 'view_expired_at',
                    # 'legal_people',
                    'status', 'show_contactor_info', 'show_shareholder_info')
    list_filter = ('status', 'ic_status', 'license_status',
                   'type', 'salesman',
                   'rating',
                   'industry',
                   'has_custom_info', 'has_customer_files',
                   'taxpayer_type', 'scale_size')
    search_fields = ('title', 'note', 'address',
                     'op_address', 'legal_people')
    inlines = [
        # ContractInline,
        ShareHolderInline,
        AttachmentInline
    ]
    form = make_ajax_form(Company, {
        'bookkeeper': 'user',
        'salesman': 'user',
        'special_taxes': 'special_taxes',
    })

    fieldsets = (
        ('公司信息', {
            'fields': ('title',
                       'industry', 'type', 'scale_size',
                       'taxpayer_type', 'rating',
                       'status', 'ic_status',
                       'has_customer_files',
                       'registered_capital',
                       'address', 'op_address',
                       'uscc', 'business_license',
                       'website', 'salesman', 'bookkeeper',
                       'registered_at', 'expired_at',
                       'tax_declared_begin',
                       'contactor', 'contactor_phone',
                       'legal_people', 'legal_phone',
                       'tags',
                       'note')
        }),

        ('申报区', {
            'fields': (
                'alias',
                'batch',
                'ss_declared',
                'tax_disk',
                'tax_username',
                'tax_password',
                'added_value_tax',
                'income_tax',
                'cut_tax',
                'invoice',
                'const_tax',
                'special_taxes',
                'declare_info', )
        }),

        ('银行信息', {
            'fields': (
                'has_czk',
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
                # 'national_tax_sn',
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
                'has_custom_info',
                'custom_register_no',
                'custom_registered_at',
                'custom_expired_at',
                'credit_rating',
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

    def changelist_view(self, request, extra_context=None):
        referrer = request.META.get('HTTP_REFERER', '')

        get_param = 'status__exact=有效'
        if len(request.GET) == 0 and '?' not in referrer:
            return redirect("{url}?{get_parms}".format(
                url=request.path,
                get_parms=get_param))
        return super(CompanyModelAdmin, self).changelist_view(
            request, extra_context=extra_context)

    actions = ['make_invalid', 'make_ic_status_invalid']

    def make_invalid(self, request, queryset):
        queryset.update(status='无效')
    make_invalid.short_description = "修改所选的公司状态为无效"

    def make_ic_status_invalid(self, request, queryset):
        queryset.update(ic_status='经营异常')
    make_ic_status_invalid.short_description = "修改工商状态为异常"

    def get_form(self, request, obj=None, **kwargs):
        form = super(CompanyModelAdmin, self).get_form(
            request, obj, **kwargs)
        if 'special_taxes' in form.base_fields:
            form.base_fields['special_taxes'].widget.attrs['style'] = 'width: 610px;'
        if 'tags' in form.base_fields:
            form.base_fields['tags'].widget.attrs['style'] = 'width: 272px;'
        return form
