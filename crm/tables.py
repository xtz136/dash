import itertools
import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html

from .models import Company, ShareHolder


class CompanyTable(tables.Table):

    class Meta:
        fields = ('title', )
        attrs = {
            'class': 'table table-striped table-bordered table-hover my-table'
        }
        default = ''

        model = Company

    def render_title(self, value, record):
        return format_html('<a href="/client/{id}/">{title}</a>'.format(
            id=record.id, title=value))

    def render_uscc(self, value, record):
        return "'" + value if value.isdigit() else value

    def render_national_tax_id(self, value, record):
        return "'" + value if value.isdigit() else value


class ShareHolderTable(tables.Table):
    class Meta:
        fields = ('role', 'name', 'phone', 'sfz', 'share')
        model = ShareHolder
        attrs = {'class': 'table table-hover'}

    def render_share(self, value):
        return '{0}%'.format(value)
