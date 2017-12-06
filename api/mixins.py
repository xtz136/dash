from rest_framework.response import Response
from rest_framework.decorators import list_route

from crm.views.mixins import SearchViewMixin


class SearchAPIViewMixin(SearchViewMixin):
    search_param = 'q'
    default_search_results = 10

    @list_route()
    def search(self, request):
        q = self.request.GET.get('q', '').strip()
        queryset = self.queryset
        if q:
            queryset = self.get_search_results(queryset, q)

        serializer = self.get_serializer(
            queryset[:self.default_search_results], many=True)
        return Response(serializer.data)
