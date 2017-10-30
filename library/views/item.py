import logging
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse

from django_tables2 import SingleTableView, SingleTableMixin
from extra_views import ModelFormSetView
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FieldWithButtons

from crm.formsets import MyTableInlineFormset
from crm.views.mixins import SearchViewMixin

from crm.models import Company

from .. import models
from .. import forms
from .. import tables
from .. import filters

log = logging.getLogger(__name__)


class LibraryView(LoginRequiredMixin, TemplateView):
    """资料库首页视图"""
    template_name = 'library.html'


class ItemReceiveView(LoginRequiredMixin,
                      PermissionRequiredMixin,
                      ModelFormSetView):
    """签收视图"""
    template_name = 'library/receive.html'
    fields = ('name', 'type', 'qty', 'note')
    model = models.Item
    permission_required = 'crm.add_item'
    raise_exception = True
    permission_denied_message = '请联系管理员获取查看该页面的权限'

    def get_queryset(self):
        return models.Item.objects.none()

    def get_formset(self):
        formset = super(ItemReceiveView, self).get_formset()
        formset.helper = MyTableInlineFormset()
        formset.helper.form_id = 'items'
        formset.helper.form_tag = False
        return formset

    def get_context_data(self, **kwargs):
        context = super(ItemReceiveView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def get_form(self):
        if self.request.method == "GET":
            return forms.ItemAutoSelectForm()
        return forms.ItemAutoSelectForm(self.request.POST)

    def post(self, *args, **kwargs):
        self.object_list = self.get_queryset()
        formset = self.construct_formset()
        form = self.get_form()
        if formset.is_valid() and form.is_valid():
            return self.formset_valid(form, formset)
        else:
            return self.formset_invalid(formset)

    def formset_valid(self, form, formset):
        self.object_list = formset.save(commit=False)
        try:
            receiver = User.objects.get(username=form.cleaned_data['receiver'])
            company = Company.objects.get(
                title=form.cleaned_data['company'])
        except:
            log.error('获取用户/公司出错', exc_info=True)
            return HttpResponseBadRequest('找不到数据')

        for obj in self.object_list:
            obj.receiver = receiver
            obj.received_at = form.cleaned_data['received_at']
            obj.company = company
            obj.save()

        # generate receipt
        receipt = models.Receipt.create_receipt(
            type='签收',
            created=form.cleaned_data['received_at'],
            user=receiver, company=company, items=self.object_list)

        return HttpResponseRedirect(
            reverse('library:receipt-detail', args=(receipt.pk,)))


class ItemBorrowView(LoginRequiredMixin, TemplateView):
    template_name = 'crm/library.html'


class ItemListView(LoginRequiredMixin,
                   SearchViewMixin,
                   SingleTableView):
    """签收资料中心"""
    template_name = 'library/item_list.html'
    model = models.Item
    table_class = tables.ItemTable
    search_fields = ('name', 'company_title', 'note')
    table_pagination = {
        'per_page': 20
    }

    def get_queryset(self):
        return self.get_search_results(
            self.model.objects.all(),
            self.request.GET.get('q', '').strip())

    def get_filter(self):
        f = filters.ItemFilter(self.request.GET, self.get_queryset())
        helper = FormHelper()
        helper.field_class = "inline"
        helper.form_tag = False
        f.form.helper = helper
        return f

    def get_search_form(self):
        f = forms.SearchForm(self.request.GET)
        helper = FormHelper()
        helper.layout = Layout(
            FieldWithButtons('q', Submit('submit', '搜索', css_class='button')))
        helper.form_show_labels = False
        helper.form_tag = False
        helper.disable_csrf = True
        f.helper = helper
        return f

    def get_context_data(self, **kwargs):
        context = super(ItemListView, self).get_context_data(**kwargs)
        context['search_form'] = self.get_search_form()
        context['filter'] = self.get_filter()
        context['borrow_form'] = forms.BorrowerAutoSelectForm()
        return context

    def get_table_data(self):
        return self.get_filter().qs


class ReceiptListView(LoginRequiredMixin, SingleTableView):
    """收据列表"""
    model = models.Receipt
    table_class = tables.ReceiptTable
    template_name = 'library/receipt_list.html'
    allow_empty = True

    def get_queryset(self):
        return self.model.objects.all()


class ReceiptDetailView(LoginRequiredMixin, SingleTableMixin, DetailView):
    """收据详细视图"""
    template_name = 'library/receipt.html'
    model = models.Receipt
    table_class = tables.ReceiptItemTable

    def get_table_data(self):
        return [o.object for o in self.object.get_items()]
