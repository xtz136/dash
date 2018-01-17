from .models import WhiteList
from django.contrib.auth import logout
from django.http import HttpResponseForbidden

from core.models import create_profile
from core.utils import get_ip


class RestrictIPMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)
        if (request.path.startswith('/wechat/')):
            return self.get_response(request)
        if user and user.is_authenticated and not user.is_superuser:
            create_profile(user)
            profile = getattr(user, 'profile', None)
            if not profile or not profile.is_manager:
                ip = get_ip(request)
                if not WhiteList.objects.filter(ip=ip).exists():
                    logout(request)
                    return HttpResponseForbidden(
                        "您当前的IP地址： {} 不允许登陆".format(ip))
        return self.get_response(request)
