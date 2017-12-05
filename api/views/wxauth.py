import time
from django.conf import settings
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import get_user_model

from wechatpy.oauth import WeChatOAuth
from rest_framework_jwt.settings import api_settings

from core.models import AccessToken

User = get_user_model()

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def issue_token(user):
    payload = jwt_payload_handler(user)
    return {
        'token': jwt_encode_handler(payload),
        'user': user
    }


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
            access_token = client.fetch_access_token(code)
            user_info = client.get_user_info()

            # 用state来关联用户
            if state and state.isdigit():
                user = User.objects.get(pk=state)
            else:
                user = User.objects.create_user(
                    username=access_token['openid'],
                    password=str(time.time()),
                    is_active=False)

            has_token = AccessToken.objects.filter(
                openid=access_token['openid']).count() == 1
            if has_token:
                AccessToken.objects.filter(
                    openid=access_token['openid']).update(user=user, **access_token)

            # update profile
            profile = create_profile(user)
            for field in ['nickname', 'sex', 'country', 'city', 'province', 'headimgurl']:
                setattr(profile, field, user_info.get(field, ''))
            profile.save()

            token = issue_token(user)['token']
            response = HttpResponse('''<html><body><h3>登录成功</h3><script>
    window.localStorage.setItem('token', '{token}');
    setTimeout(function () {
        window.location = "/dashboard";
    }, 2000)
</script></body></html>'''.format(token=token))
            response.set_cookie('token', token)
            return response
        except Exception as e:
            print(e)

    return redirect(client.authorize_url)

# 微信授权回调接口


def wx_auth(request):
    code = request.GET.get('code', '')
    if code:
        api = WeChatClient(settings.WX_APPID,
                           settings.WX_APPSECRET)
        try:
            user_info = api.oauth.get_user_info(code)
        except Exception as e:
            print(e)

        import pdb
        pdb.set_trace()

        token = 'this is token'
    return redirect('/api/wx/login/')
