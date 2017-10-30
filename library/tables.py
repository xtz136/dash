import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html

from .models import Item, Receipt


class ReceiptTable(tables.Table):
    action = tables.Column(verbose_name="动作", accessor="pk")

    def __init__(self, *args, **kwargs):
        super(ReceiptTable, self).__init__(*args, **kwargs)

    class Meta:
        model = Receipt
        fields = ('company', 'type', 'user', 'created', 'items', 'action')
        attrs = {'class': 'table table-striped table-bordered table-hover my-table'}

    def render_row_number(self):
        return next(self.counter)

    def render_action(self, value, record):
        return format_html('<a href="{0}">打印收据<i class="fa fa-print"></i></a>'.format(reverse('library:receipt-detail', args=(value,))))

    def render_created(self, value, record):
        return value.strftime("%Y-%m-%d")

    def render_items(self, value, record):
        return format_html('<br />'.join(['{0} x {1}'.format(o.object.name, o.object.qty) for o in record.get_items()]))


class ReceiptItemTable(tables.Table):
    class Meta:
        model = Item
        fields = ('company', 'name', 'type', 'qty')
        attrs = {'class': 'table nvoice-table'}
        orderable = False


class ItemTable(tables.Table):
    id = tables.Column(
        verbose_name=format_html('<input type="checkbox" id="action-toggle">'))

    class Meta:
        model = Item
        fields = ('id', 'company_title', 'name', 'type',
                  'qty', 'note', 'status', 'received_at')
        attrs = {'class': 'table table-hover no-margins table-responsive'}

    def render_id(self, value):
        return format_html('<input type="checkbox" value="{0}" class="action-select" />'.format(value))

    def has_footer(self):
        return True

    def footer_empty(self):
        return True
