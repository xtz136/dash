import time
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse
from django.http.response import JsonResponse, HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.contrib.auth import authenticate, login

from api.serializers import UserSerializer
from wechatpy.oauth import WeChatOAuth

from core.models import AccessToken, create_profile, SiteConf

User = get_user_model()


def authorize(request):
    code = request.GET.get('code', '')
    # use state to track user id
    state = request.GET.get('state', '')
    config = SiteConf.get_solo()

    if not config.enable_wechat:
        return HttpResponseForbidden('没有开启微信登录')

    client = WeChatOAuth(config.wx_appid,
                         config.wx_appsecret,
                         config.wx_redirect_uri,
                         scope='snsapi_userinfo',
                         state=state)

    # auth flow
    if code:
        try:
            access_token = client.fetch_access_token(code)
            user_info = client.get_user_info()
            # get or create access_token
            at, _ = AccessToken.objects.get_or_create(
                openid=access_token['openid'])
            if not at.user:
                at.user = User.objects.create(
                    username='wx_' + access_token['openid'],
                    is_active=True)

            at.update_token(access_token)
            user = at.user

            # update profile
            user.profile.update_profile(user_info)
            login(request, user)
            request.session.set_expiry(3600 * 24 * 7)  # 7days
            return redirect('wechat:index')
        except Exception as e:
            return HttpResponseForbidden('发生错误 {0}'.format(str(e)))

    return redirect(client.authorize_url)
