from .models import WhiteList
from django.contrib.auth import logout
from django.http import HttpResponseForbidden

IPWARE_META_PRECEDENCE_ORDER = (
    'HTTP_X_FORWARDED_FOR', 'X_FORWARDED_FOR',  # client, proxy1, proxy2
    'HTTP_CLIENT_IP',
    'HTTP_X_REAL_IP',
    'HTTP_X_FORWARDED',
    'HTTP_X_CLUSTER_CLIENT_IP',
    'HTTP_FORWARDED_FOR',
    'HTTP_FORWARDED',
    'HTTP_VIA',
    'REMOTE_ADDR',
)


def get_ip(request):
    # best match ip
    for key in IPWARE_META_PRECEDENCE_ORDER:
        if request.META.get(key, None):
            return request.META[key]
    return None


class RestrictIPMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)
        if user and not user.is_superuser:
            profile = getattr(user, 'profile', None)
            if profile and not profile.is_manager:
                ip = get_ip(request)
                is_banned = False
                try:
                    WhiteList.objects.get(ip=ip)
                except WhiteList.DoesNotExist:
                    is_banned = True

                if is_banned:
                    logout(request)
                    return HttpResponseForbidden(
                        "您当前的IP地址： {} 不允许登陆".format(ip))
        return self.get_response(request)
