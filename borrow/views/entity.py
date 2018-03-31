from ._base import ApiView, Pagination
from ..models.entity import Entity


class EntityApiView(ApiView, Pagination):

    """有关实体清单的接口"""

    _search_fields = ()
    _default_order = '-id'
    _list_fields = ('id', 'name')

    def api_filter(self, request, args):
        search = Entity.objects.all()
        result = self.decode(search)
        return self.success(result)
