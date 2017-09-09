from django.contrib import admin

from crm.models import Contract
from .common import AttachmentInline


class ContractInline(admin.TabularInline):
    model = Contract


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
