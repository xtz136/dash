from ._base import ApiView, Pagination
from django.contrib.auth.models import User
from django.db.models import Q


class PeopleApiView(ApiView, Pagination):

    """有关人员的接口"""

    _search_fields = ('name')
    _default_order = '-id'
    _list_fields = ('id', 'first_name', 'last_name')

    def api_filter(self, request, args):
        cond = Q(
            first_name__contains=args['name']) | Q(
            last_name__contains=args['name'])
        search = User.objects.filter(cond)
        result = self.decode(search)
        return self.success(result)
