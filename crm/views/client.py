import logging
import operator
from functools import reduce

from django.views.generic import TemplateView, DetailView, UpdateView, CreateView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.forms import inlineformset_factory, modelformset_factory, all_valid

from django_tables2 import Column
from crispy_forms.helper import FormHelper, Layout
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSet
from extra_views.generic import GenericInlineFormSet

from .. import filters
from .. import tables
from .. import models
from .. import forms
from .formsets import MyFormsetHelper
from core.models import Attachment


logger = logging.getLogger(__name__)


def construct_search(field_name):
    if field_name.startswith('^'):
        return "%s__istartswith" % field_name[1:]
    elif field_name.startswith('='):
        return "%s__iexact" % field_name[1:]
    elif field_name.startswith('@'):
        return "%s__search" % field_name[1:]
    else:
        return "%s__icontains" % field_name


class SearchViewMixin:
    search_fields = None

    def get_search_results(self, queryset, search_term):
        if search_term and self.search_fields:
            orm_lookups = map(construct_search, self.search_fields)
            for bit in search_term.split():
                or_queries = [Q(**{orm_lookup: bit})
                              for orm_lookup in orm_lookups]
                queryset = queryset.filter(reduce(operator.or_, or_queries))
        return queryset


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

    def get_context_data(self, **kwargs):
        context = super(ClientSearchView, self).get_context_data(**kwargs)
        objects = models.Company.objects.none()
        q = self.request.GET.get('q', '').strip()

        queryset = models.Company.objects.none()
        if q:
            queryset = self.get_search_results(
                models.Company.objects.all(), q)

        context['filter'] = self.get_filter(queryset)
        context['search_form'] = forms.SearchForm(data=self.request.GET)
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
        formset.helper = MyFormsetHelper()
        formset.helper.form_id = 'shareholder_set'
        return formset


class AttachmentInline(GenericInlineFormSet):
    model = Attachment
    form_class = forms.AttachmentModelForm

    def construct_formset(self):
        formset = super(AttachmentInline, self).construct_formset()
        formset.helper = MyFormsetHelper()
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
