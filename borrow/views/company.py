from ._base import ApiView, Pagination
from crm.models.company import Company


class CompanyApiView(ApiView, Pagination):

    """有关公司的接口"""

    _search_fields = ('title')
    _default_order = '-id'

    def api_list(self, request, args):
        search = Company.objects
        result = self.pagination(request, search)
        return self.success(result)
