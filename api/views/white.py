from security.models import WhiteList
from django.http import JsonResponse
from django.conf import settings

from core.utils import get_ip


def update_white_list_request(request):
    token = request.GET.get('token', None)
    if settings.SIGN_TOKEN == token:
        ip = get_ip(request)
        WhiteList.objects.get_or_create(ip=ip)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'failed'})
