from crm.models.company import Company
from ._base import ApiView, Pagination, CheckPerm
from ..perm_types import revert_list_perm
from ..models import revert_list


class RevertListApiView(ApiView, Pagination):

    """有关归还单的接口"""

    _search_fields = (
        ('order_id', 'order_id__contains'),
        ('company', 'company'))
    _default_order = '-id'
    _list_fields = (
        'id',
        'order_id',
        'company',
        'revert_borrow_date')

    @CheckPerm.check(revert_list_perm.view)
    def api_filter(self, request, args):
        # 先搜索一次公司表
        if args.get('company'):
            company = Company.objects.get(title__contains=args['company'])
            if company:
                args['company'] = company
            else:
                del args['company']

        filter_query = self.get_filter_query(args)
        search = revert_list.RevertList.objects.filter(**filter_query)
        result = self.pagination(args, search)
        return self.success(result)
