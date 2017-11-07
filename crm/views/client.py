import logging
from datetime import datetime
from collections import namedtuple

from django.views.generic import TemplateView, DetailView, UpdateView, CreateView, FormView
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.forms import inlineformset_factory, modelformset_factory, all_valid
from django.contrib.auth.models import User

import xlrd
from django_tables2 import Column
from crispy_forms.helper import FormHelper, Layout
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSet
from extra_views.generic import GenericInlineFormSet

from .. import filters
from .. import tables
from .. import models
from .. import forms
from ..formsets import MyTableInlineFormset
from .mixins import SearchViewMixin
from core.models import Attachment


logger = logging.getLogger(__name__)


class ClientSearchView(SearchViewMixin, LoginRequiredMixin, TemplateView):
    template_name = 'crm/client/index.html'
    search_fields = ('title', 'note', 'address',
                     'op_address', 'legal_people')

    def get_filter(self, queryset):
        _filter = filters.CompanyFilter(self.request.GET, queryset=queryset)
        helper = FormHelper()
        helper.form_class = 'form-inline'
        helper.form_tag = False
        helper.layout = Layout(
            'status',
            'ic_status',
            'license_status',
        )
        _filter.form.helper = helper

        return _filter

    def get_search_form(self):
        return forms.AutoCompanyForm(data=self.request.GET)

    def get_context_data(self, **kwargs):
        context = super(ClientSearchView, self).get_context_data(**kwargs)
        objects = models.Company.objects.none()
        q = self.request.GET.get('q', '').strip()

        queryset = models.Company.objects.none()
        if q:
            queryset = self.get_search_results(
                models.Company.objects.all(), q)

        context['filter'] = self.get_filter(queryset)
        context['search_form'] = self.get_search_form()
        extra_columns = [(i, Column()) for i in
                         self.request.user.profile.preference.get(
                             'company_list_fields', ['status'])]
        context['table'] = tables.CompanyTable(context['filter'].qs,
                                               extra_columns=extra_columns)
        pre_form = forms.PreferenceForm(
            data=self.request.user.profile.preference)

        context['pre_form'] = pre_form
        context['has_add_perm'] = self.request.user.has_perm('crm.add_company')
        return context


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = models.Company
    template_name = "crm/client/detail.html"

    def get_context_data(self, **kwargs):
        context = super(ClientDetailView, self).get_context_data(**kwargs)
        context['form'] = forms.CompanyModelForm(
            instance=context['object'], readonly=True)
        context['shareholder_table'] = tables.ShareHolderTable(
            self.object.shareholder_set.all())
        context['has_change_perm'] = self.request.user.has_perm(
            'crm.change_company')
        return context


class ShareHolderInline(InlineFormSet):
    model = models.ShareHolder
    form_class = forms.ShareHolderModelForm

    def construct_formset(self):
        formset = super(ShareHolderInline, self).construct_formset()
        formset.helper = MyTableInlineFormset()
        formset.helper.form_id = 'shareholder_set'
        return formset


class AttachmentInline(GenericInlineFormSet):
    model = Attachment
    form_class = forms.AttachmentModelForm

    def construct_formset(self):
        formset = super(AttachmentInline, self).construct_formset()
        formset.helper = MyTableInlineFormset()
        formset.helper.form_id = 'attachments'
        return formset


class ClientEditView(LoginRequiredMixin,
                     PermissionRequiredMixin,
                     UpdateWithInlinesView):
    model = models.Company
    template_name = "crm/client/edit.html"
    form_class = forms.CompanyModelForm
    permission_required = 'crm.change_company'
    raise_exception = True
    permission_denied_message = '请联系管理员获取查看该页面的权限'
    inlines = [ShareHolderInline, AttachmentInline]

    def get_success_url(self):
        logger.info('编辑完成')
        return reverse('crm:client-detail', kwargs={'pk': self.object.pk})


class ClientCreateView(LoginRequiredMixin,
                       PermissionRequiredMixin,
                       CreateWithInlinesView):

    model = models.Company
    template_name = "crm/client/create.html"
    form_class = forms.CompanyModelForm
    permission_required = 'crm.add_company'
    raise_exception = True
    permission_denied_message = '请联系管理员获取查看该页面的权限'
    inlines = [ShareHolderInline, AttachmentInline]

    def get_success_url(self):
        return reverse('crm:client-detail', kwargs={'pk': self.object.pk})


class BatchClientUpdateView(LoginRequiredMixin,
                            PermissionRequiredMixin,
                            FormView):
    """批量更新客户信息，模板格式必须约定好"""
    template_name = 'crm/client/batch.html'
    form_class = forms.BatchClientUpdateForm
    permission_required = 'crm.add_company'
    raise_exception = True
    permission_denied_message = '请联系管理员获取查看该页面的权限'
    field_types = {
        'ss_date': 'date',
        'registered_at': 'date',
        'custom_expired_at': 'date',
        'custom_registered_at': 'date',
        'salesman': 'user',
    }

    def parse_sheet(self, contents):
        book = xlrd.open_workbook(file_contents=contents)
        sheet = book.sheet_by_index(0)
        names = sheet.row_values(0)

        fields = [
            f.name for name in names
            for f in models.Company._meta.fields if f.verbose_name == name
        ]

        # 错误的模板
        if len(fields) != len(names):
            raise ValueError(fields, names)

        ClientRecord = namedtuple('ClientRecord', fields)
        n = 0

        for i in range(1, sheet.nrows):
            row = self.__format(ClientRecord(*sheet.row_values(i))._asdict())

            qs = models.Company.objects.filter(title=row['title'])

            # try with starts
            if not qs.exists():
                qs = models.Company.objects.filter(
                    title__startswith=row['title'])
                logger.info(row['title'])

            # only update match
            if qs.count() == 1:
                qs.update(**row)
                n += 1
            else:
                logger.warn("{} not found".format(row['title']))
        return (sheet.nrows - 1, n)

    def __format(self, row):
        """将特殊的字段转换"""
        for field, value in row.items():
            m = '_format_' + field
            if hasattr(self, m):
                row[field] = getattr(self, m)(value)
        return row

    def _format_custom_expired_at(self, value):
        return xlrd.xldate.xldate_as_datetime(value, 0) if value else None

    def _format_ss_date(self, value):
        return xlrd.xldate.xldate_as_datetime(value, 0) if value else None

    def _format_salesman(self, value):
        return User.objects.get(username=value) if value else None

    def _format_bookkeeper(self, value):
        return User.objects.get(username=value) if value else None

    def _format_registered_at(self, value):
        if not value or not value.strip("—"):
            return None
        return datetime.strptime(value.strip(), "%Y年%m月%d日")

    def _format_custom_registered_at(self, value):
        return xlrd.xldate.xldate_as_datetime(value, 0) if value else None

    def form_valid(self, form):
        rows, parsed = self.parse_sheet(form.cleaned_data['file'].read())
        return HttpResponse("{} rows, updated {} ".format(rows, parsed))
