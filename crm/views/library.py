import logging
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse

from django_tables2 import SingleTableView, SingleTableMixin
from extra_views import ModelFormSetView
from crispy_forms.helper import FormHelper

from .formsets import MyFormsetHelper

from .. import models
from .. import forms
from .. import tables

log = logging.getLogger(__name__)


class ReceiveView(LoginRequiredMixin,
                  PermissionRequiredMixin,
                  ModelFormSetView):
    template_name = 'crm/library/receive.html'
    fields = ('name', 'type', 'qty', 'note')
    model = models.Item
    permission_required = 'crm.add_item'
    raise_exception = True
    permission_denied_message = '请联系管理员获取查看该页面的权限'

    def get_queryset(self):
        return models.Item.objects.none()

    def get_formset(self):
        formset = super(ReceiveView, self).get_formset()
        formset.helper = MyFormsetHelper()
        formset.helper.form_id = 'items'
        formset.helper.form_tag = False
        return formset

    def get_context_data(self, **kwargs):
        context = super(ReceiveView, self).get_context_data(**kwargs)
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
            company = models.Company.objects.get(
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
            reverse('crm:library-receipt-detail', args=(receipt.pk,)))


class LibraryView(LoginRequiredMixin, TemplateView):
    template_name = 'crm/library.html'


class BorrowView(LoginRequiredMixin, TemplateView):
    template_name = 'crm/library.html'


class ManageView(LoginRequiredMixin, TemplateView):
    template_name = 'crm/library.html'


class ReceiptListView(LoginRequiredMixin, SingleTableView):
    model = models.Receipt
    table_class = tables.ReceiptTable
    template_name = 'crm/library/list.html'
    allow_empty = True

    def get_queryset(self):
        return self.model.objects.all()


class ReceiptDetailView(LoginRequiredMixin, SingleTableMixin, DetailView):
    template_name = 'crm/library/receipt.html'
    model = models.Receipt
    table_class = tables.ReceiptItemTable

    def get_table_data(self):
        return [o.object for o in self.object.get_items()]
