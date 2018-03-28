import json
import logging

from django.db.models import Model
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.views.generic import View
from django.db.models.query import QuerySet
from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder

log = logging.getLogger('BaseApi')


class ModelEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Model):
            return model_to_dict(obj)
        elif isinstance(obj, QuerySet):
            return list(obj)
        else:
            return DjangoJSONEncoder.default(self, obj)


class ApiView(View):

    """方便输出json数据
    """

    def post(self, request):
        """ 某个功能的接口分发方法，接口只能通过post方式调用
        Args:
            api_type(str): 指定调用哪个接口
            api_data(any): 指定接口的参数，一般是字典类型
        """
        api_type = request.POST.get('type', 'api_empty')
        api_data = request.POST.get('data', None) or '{}'

        method = getattr(self, api_type, None)
        if method is None:
            return self.failed('api not found.')

        log.info(
            'call api. name => {}, method => {}'.format(type(self).__name__, api_type))

        try:
            return method(request, json.loads(api_data))
        except Exception:
            log.exception(
                'api error. method => {}, data => {}'.format(api_type, api_data))
            return self.failed('api error.')

    def success(self, msg, code=0):
        """ 接口执行成功
        Args:
            msg(any): 接口放回给前端的数据
            code(int): 接口的返回值，默认是0
        Return:
            JSON({msg: msg, code: code, status: True})
        """
        result = json.dumps({'msg': msg, 'code': code, 'status': True}, cls=ModelEncoder)
        return HttpResponse(result, content_type="application/json")

    def failed(self, msg, code=-1):
        """ 接口执行失败
        Args:
            msg(any): 接口放回给前端的数据
            code(int): 接口的返回值，默认是-1
        Return:
            JSON({msg: msg, code: code, status: False})
        """
        result = json.dumps({'msg': msg, 'code': code, 'status': False}, cls=ModelEncoder)
        return HttpResponse(result, content_type="application/json")


class Pagination:

    """分页"""

    _page_size = 10
    _search_fields = []
    _default_order = ''

    def pagination(self, request, object_list):
        page_num = request.POST.get('page', 1)
        try:
            page_num = int(page_num)
        except Exception:
            page_num = 1

        order_by = request.POST.get('order_by', self._default_order)
        if order_by:
            object_list = object_list.order_by(order_by)

        page_size = request.POST.get('page_size', self._page_size)

        p = Paginator(object_list, page_size)
        page = p.page(page_num)

        return {
            'count': p.count,
            'page_count': p.num_pages,
            'datas': page.object_list,
            'page': page.number,
            'has_prev': page.has_previous(),
            'has_next': page.has_next()
        }
