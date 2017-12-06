import time
from django.conf import settings
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from wechatpy.oauth import WeChatOAuth
from rest_framework_jwt.settings import api_settings

from core.models import AccessToken, create_profile

User = get_user_model()

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def issue_token(user):
    payload = jwt_payload_handler(user)
    return {
        'token': jwt_encode_handler(payload),
        'user': user
    }


tpl = '''<html><body>
<h3>登录成功</h3>
<script>
  window.localStorage.setItem('token', '%(token)s');
  setTimeout(function () {
    window.location = "/dashboard";
  }, 2000);
</script></body></html>'''


def authorize(request):
    code = request.GET.get('code', '')
    # use state to track user id
    state = request.GET.get('state', '')

    client = WeChatOAuth(settings.WX_APPID,
                         settings.WX_APPSECRET,
                         settings.WX_REDIRECT_URI,
                         scope='snsapi_userinfo',
                         state=state)

    # auth flow
    if code:
        try:
            # may raise
            access_token = client.fetch_access_token(code)
            user_info = client.get_user_info()

            # 用state来关联用户
            if state and state.isdigit():
                user = User.objects.get(pk=state)
            else:
                user, _ = User.objects.get_or_create(
                    username='wx_' + access_token['openid'])

            # may raise IntegrityError 微信用户已经绑定了关系
            at, _ = AccessToken.objects.get_or_create(
                user=user, openid=access_token['openid'])
            at.update_token(access_token)

            # update profile
            user.profile.update_profile(user_info)
            token = issue_token(user)
            response = HttpResponse(tpl % token)
            response.set_cookie('token', token)
            return response
        except IntegrityError:
            return HttpResponse('用户已经绑定了微信账号', status=400)
        except Exception as e:
            return HttpResponse('failed {0}'.format(e), status=500)

    return redirect(client.authorize_url)
