from ._base import ApiView, Pagination
from ..models.entity_list import EntityList


class EntityListApiView(Pagination, ApiView):

    """有关实体清单的接口"""

    _search_fields = ('')
    _default_order = '-id'
    _list_fields = (
        'id',
        ('entity', 'name'),
        'amount',
        ('signer', 'username'),
        'sign_date',
        ('borrower', 'username'),
        'borrow_date',
        'revert_borrow_date',
        'revert_date',
        'status',
        'descript')

    def api_list(self, request, args):
        search = EntityList.objects
        result = self.pagination(request, search)
        return self.success(result)

    def api_filter(self, request, args):
        search = EntityList.objects.filter(company_id=args['companyId'])
        result = self.pagination(request, search)
        return self.success(result)

    def api_add(self, request, args):
        model = args['entityList']
        entity_list = EntityList.objects.create(**model)
        entity_list.save()
        return self.success(entity_list.id)
