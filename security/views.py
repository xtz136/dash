from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings
from django.shortcuts import render

from .models import WhiteList


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_REAL_IP')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def update_whitelist_view(request):
    ip = get_client_ip(request)
    token = request.GET.get("token", "")
    if token == settings.UPDATE_WHITELIST_TOKEN:
        WhiteList.objects.create(ip=ip)
        return HttpResponse("ok")
    return HttpResponseForbidden("you are not welcome.")
