from ._base import ApiView, Pagination
from ..models.entity import Entity


class EntityApiView(ApiView, Pagination):

    """有关实体清单的接口"""

    _search_fields = ('name')
    _default_order = '-id'
    _list_fields = ('id', 'name')

    def api_list(self, request, args):
        search = Entity.objects
        result = self.pagination(request, search)
        return self.success(result)
