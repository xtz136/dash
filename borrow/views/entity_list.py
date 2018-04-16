from ._base import ApiView, Pagination, CheckPerm
from ..perm_types import entity_list_perm, revert_list_perm
from ..models.entity_list import EntityList
from ..models.revert_list import RevertList


class EntityListApiView(Pagination, ApiView):

    """有关实体清单的接口"""

    _search_fields = (
        ('status', 'status'),
        ('signer_id', 'signer_id'),
        ('sign_date', 'sign_date__range'),
        ('company_id', 'company_id'),
        ('descript', 'descript'),
        ('order_id', 'ordeer_id__contains'),
        ('entity_id', 'entity_id'),
        ('borrow_id', 'borrow_id'),
        ('borrow_date', 'borrow_date__range'),
        ('revert_date', 'revert_date__range')
    )
    _default_order = '-id'
    _list_fields = (
        'id',
        ('entity#name', 'entity'),
        'entity_id',
        'amount',
        'signer',
        'signer_id',
        'sign_date',
        'borrower',
        'borrower_id',
        'borrow_date',
        'revert_borrow_date',
        'revert_date',
        'status',
        'descript')

    @CheckPerm.check(entity_list_perm.view)
    def api_filter(self, request, args):
        filter_query = self.get_filter_query(args)
        search = EntityList.objects.filter(**filter_query)
        result = self.pagination(args, search)
        return self.success(result)

    @CheckPerm.check(entity_list_perm.view)
    def api_filter_all(self, request, args):
        filter_query = self.get_filter_query(args)
        status = filter_query.pop('status', None)
        search = EntityList.objects.filter(**filter_query)
        if status:
            search = search.exclude(status=status)
        result = self.decode(search)
        return self.success(result)

    @CheckPerm.check(entity_list_perm.add)
    def api_update(self, request, args):
        datas = args['datas']
        results = []

        for update in datas:
            model = {}
            for field in EntityList._meta.get_fields():
                name = field.name
                if field.is_relation:
                    name = name + '_id'
                if name not in update:
                    continue
                model[name] = update[name]

            if model.get('id'):
                result = model.pop('id')
                EntityList.objects.filter(pk=result).update(**model)
            else:
                entity_list = EntityList.objects.create(**model)
                entity_list.save()
                result = entity_list.id

            results.append(result)

        return self.success(results)

    @CheckPerm.check(entity_list_perm.add)
    def api_revert(self, request, args):
        if not args.get('selected'):
            return self.failed('没有选择归还物品', 2)

        # 生成订单编号
        order_id = RevertList.create(args['company_id'])

        EntityList.objects.filter(
            pk__in=args['selected']).update(
            status='归还', order_id=order_id)

        return self.success(order_id)

    @CheckPerm.check(revert_list_perm.view)
    def api_get_revert(self, request, args):
        revert_list_id = args.get('id')
        if not revert_list_id:
            return self.failed('参数错误', 3)

        search = EntityList.objects.filter(order_id_id=revert_list_id)
        result = self.decode(search)
        return self.success(result)
