from django.contrib import admin
from django.utils.safestring import mark_safe

from crm.models import TaxBureau


@admin.register(TaxBureau)
class TaxBureauModelAdmin(admin.ModelAdmin):
    search_fields = ('full_title', 'address')
    list_filter = ('district', 'bureau')
    list_display = ('full_title', 'bureau', 'view_map')

    def view_map(self, obj):
        return mark_safe(
            "<a href='http://api.map.baidu.com/geocoder?address={0}&output=html' target='_blank'>查看地图</a>"
            .format(obj.full_title))
    view_map.short_description = '查看地图信息'
