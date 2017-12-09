import operator
from functools import reduce

from django.db.models import Q


def construct_search(field_name):
    if field_name.startswith('^'):
        return "%s__istartswith" % field_name[1:]
    elif field_name.startswith('='):
        return "%s__iexact" % field_name[1:]
    elif field_name.startswith('@'):
        return "%s__search" % field_name[1:]
    else:
        return "%s__icontains" % field_name


class SearchFilter:
    search_param = 'q'

    def filter_queryset(self, request, queryset, view):
        search_fields = getattr(view, 'search_fields', None)
        if not search_fields:
            raise ValueError("search_fields must defined")
        search_param = getattr(view, 'search_param', self.search_param)
        q = request.GET.get(search_param, '').strip()
        if q:
            queryset = self.get_search_results(queryset, q, search_fields)
        return queryset

    def get_search_results(self, queryset, search_term, search_fields):
        orm_lookups = [construct_search(i) for i in search_fields]
        for bit in search_term.split():
            or_queries = [Q(**{orm_lookup: bit})
                          for orm_lookup in orm_lookups]
            queryset = queryset.filter(reduce(operator.or_, or_queries))
        return queryset
