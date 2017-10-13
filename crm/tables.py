import itertools
import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html

from .models import Company, ShareHolder, Receipt, Item


class CompanyTable(tables.Table):

    class Meta:
        fields = ('title', )
        attrs = {
            'class': 'table table-striped table-bordered table-hover my-table'
        }

        model = Company

    def render_title(self, value, record):
        return format_html('<a href="/client/{id}/">{title}</a>'.format(
            id=record.id, title=value))


class ShareHolderTable(tables.Table):
    class Meta:
        fields = ('role', 'name', 'phone', 'sfz', 'share')
        model = ShareHolder
        attrs = {'class': 'table table-hover'}

    def render_share(self, value):
        return '{0}%'.format(value)


class ReceiptTable(tables.Table):
    action = tables.Column(verbose_name="动作", accessor="pk")

    def __init__(self, *args, **kwargs):
        super(ReceiptTable, self).__init__(*args, **kwargs)
        self.counter = next(itertools.count())

    class Meta:
        model = Receipt
        fields = ('company', 'type', 'user', 'created', 'items', 'action')
        attrs = {'class': 'table table-striped table-bordered table-hover my-table'}

    def render_row_number(self):
        return next(self.counter)

    def render_action(self, value, record):
        return format_html('<a href="{0}">打印收据<i class="fa fa-print"></i></a>'.format(reverse('crm:library-receipt-detail', args=(value,))))

    def render_created(self, value, record):
        return value.strftime("%Y-%m-%d")

    def render_items(self, value, record):
        return format_html('<br />'.join(['{0} x {1}'.format(o.object.name, o.object.qty) for o in record.get_items()]))


class ReceiptItemTable(tables.Table):
    class Meta:
        model = Item
        fields = ('company', 'name', 'type', 'qty')
        attrs = {'class': 'table invoice-table'}
        orderable = False
