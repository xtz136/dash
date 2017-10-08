import itertools
import django_tables2 as tables
from django.utils.safestring import mark_safe

from .models import Company, ShareHolder


class CompanyTable(tables.Table):

    class Meta:
        fields = ('title', )
        attrs = {
            'class': 'table table-striped table-bordered table-hover my-table'
        }

        model = Company

    def render_title(self, value, record):
        return mark_safe('<a href="/client/{id}/">{title}</a>'.format(
            id=record.id, title=value))


class ShareHolderTable(tables.Table):
    class Meta:
        fields = ('role', 'name', 'phone', 'sfz', 'share')
        model = ShareHolder
        attrs = {'class': 'table table-hover'}

    def render_share(self, value):
        return '{0}%'.format(value)
