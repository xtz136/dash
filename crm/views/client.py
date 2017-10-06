import operator
from django.views.generic import TemplateView, DetailView, UpdateView, CreateView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from functools import reduce
from django_tables2 import Column

from .. import tables
from .. import models
from .. import forms


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


class ClientView(SearchViewMixin, LoginRequiredMixin, TemplateView):
    template_name = 'crm/client/index.html'
    search_fields = ('title', 'note', 'address',
                     'op_address', 'legal_people')

    def get_context_data(self, **kwargs):
        context = super(ClientView, self).get_context_data(**kwargs)
        objects = models.Company.objects.none()
        q = self.request.GET.get('q', '').strip()
        if q:
            objects = self.get_search_results(
                models.Company.objects.all(), q)

        context['search_form'] = forms.SearchForm(data=self.request.GET)
        extra_columns = [(i, Column()) for i in
                         self.request.user.profile.preference.get('company_list_fields', [
                             'id', 'title', 'status'])]
        context['table'] = tables.CompanyTable(
            objects, extra_columns=extra_columns)
        pre_form = forms.PreferenceForm(
            data=self.request.user.profile.preference)

        context['pre_form'] = pre_form
        context['has_add_perm'] = self.request.user.has_perm('crm.add_company')
        context['nav_item'] = 'client'
        return context


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = models.Company
    template_name = "crm/client/detail.html"

    def get_context_data(self, **kwargs):
        context = super(ClientDetailView, self).get_context_data(**kwargs)
        context['form'] = forms.CompanyModelForm(
            instance=context['object'], readonly=True)
        context['has_change_perm'] = self.request.user.has_perm(
            'crm.change_company')
        return context


class ClientEditView(LoginRequiredMixin,
                     PermissionRequiredMixin,
                     UpdateView):
    model = models.Company
    template_name = "crm/client/edit.html"
    form_class = forms.CompanyModelForm

    permission_required = 'crm.change_company'
    raise_exception = True
    permission_denied_message = '请联系管理员获取查看该页面的权限'

    def get_success_url(self):
        return reverse('crm:client-detail', kwargs={'pk': self.object.pk})


class ClientCreateView(LoginRequiredMixin,
                       PermissionRequiredMixin,
                       CreateView):
    model = models.Company
    template_name = "crm/client/create.html"
    form_class = forms.CompanyModelForm

    raise_exception = True
    permission_denied_message = '请联系管理员获取查看该页面的权限'
    permission_required = 'crm.add_company'

    def get_success_url(self):
        return reverse('crm:client-detail', kwargs={'pk': self.object.pk})
