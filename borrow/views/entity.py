from ._base import ApiView, Pagination, CheckPerm
from ..perm_types import entity_perm
from ..models.entity import Entity


class EntityApiView(ApiView, Pagination):

    """有关实体清单的接口"""

    _search_fields = ()
    _default_order = '-id'
    _list_fields = ('id', 'name')

    @CheckPerm.check(entity_perm.view)
    def api_filter(self, request, args):
        search = Entity.objects.all()
        result = self.decode(search)
        return self.success(result)
