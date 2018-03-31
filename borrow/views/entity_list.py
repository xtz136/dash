from datetime import datetime
from django.db.models import F

from ._base import ApiView, Pagination
from ..models.entity_list import EntityList
from ..models.order import Order


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

    def api_filter(self, request, args):
        filter_query = self.get_filter_query(args)
        search = EntityList.objects.filter(**filter_query)
        result = self.pagination(args, search)
        return self.success(result)

    def api_filter_all(self, request, args):
        filter_query = self.get_filter_query(args)
        status = filter_query.pop('status', None)
        search = EntityList.objects.filter(**filter_query)
        if status:
            search = search.exclude(status=status)
        result = self.decode(search)
        return self.success(result)

    def api_update(self, request, args):
        update = args['entityList']

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

        return self.success(result)

    def api_revert(self, request, args):
        if not args.get('selected'):
            return self.failed('没有选择归还物品', 2)

        # 生成订单编号
        order_id = self.get_order_id()

        EntityList.objects.filter(
            pk__in=args['selected']).update(
            status='归还', order_id=order_id)

        return self.success(order_id)

    def get_order_id(self):
        now = datetime.now()
        date_str = now.strftime('%Y-%m-%d')

        order, _ = Order.objects.get_or_create(date=date_str)
        order.order_id = F('order_id') + 1
        order.save()

        order.refresh_from_db()
        order_id = str(order.order_id).zfill(4)

        return 'YH{}{}'.format(date_str.replace('-', ''), order_id)
