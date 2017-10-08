from django.db import models
from django.contrib import admin
from django.forms import Textarea

from ajax_select import make_ajax_form

from crm.models import ShareHolder


@admin.register(ShareHolder)
class ShareHolderModelAdmin(admin.ModelAdmin):
    search_fields = ('company_title',  'info')
    list_display = ('company_title', 'phone', 'role',
                    'view_share', 'is_contactor')
    list_filter = ('is_contactor', )
    form = make_ajax_form(ShareHolder, {
        'company': 'company',
    })

    def view_share(self, obj):
        return '{:.2f}%'.format(obj.share)
    view_share.short_description = '占比'


class ShareHolderInline(admin.TabularInline):
    model = ShareHolder
    extra = 1
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 40})}
    }
