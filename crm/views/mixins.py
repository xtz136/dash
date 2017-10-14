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
