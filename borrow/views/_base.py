import json
import logging

from django.views.generic import View
from django.shortcuts import render
from django.http import JsonResponse

log = logging.getLogger('BaseApi')


class ApiView(View):

    """方便输出json数据
    """

    template_name = 'index.html'

    def get(self, request):
        """ 输出某个功能的html页面
        """
        return render(request, self.template_name)

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
        return JsonResponse({'msg': msg, 'code': code, 'status': True})

    def failed(self, msg, code=-1):
        """ 接口执行失败
        Args:
            msg(any): 接口放回给前端的数据
            code(int): 接口的返回值，默认是-1
        Return:
            JSON({msg: msg, code: code, status: False})
        """
        return JsonResponse({'msg': msg, 'code': code, 'status': False})
