"""
Appid: wx281a91e325cfb67f
AppSecret: f0327ea2669606b9c97b7347eb19ec27
"""

from django.conf import settings
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import get_user_model


from wechatpy.oauth import WeChatOAuth

from core.models import AccessToken

User = get_user_model()


def authorize(request):
    client = WeChatOAuth(settings.WX_APPID,
                         settings.WX_APPSECRET,
                         settings.WX_REDIRECT_URI,
                         scope='snsapi_userinfo',
                         state=state)
    code = request.GET.get('code', '')

    # use state to track user id
    state = int(request.GET.get('state', ''))

    # auth flow
    if code and state.isdigit():
        try:
            access_token = client.fetch_access_token(code)
            user_info = client.get_user_info()
            user = User.objects.get(pk=state)

            has_token = AccessToken.objects.filter(
                openid=access_token['openid']).count() == 1
            if has_token:
                AccessToken.objects.filter(
                    openid=access_token['openid']).update(user=user, **access_token)

            # update profile
            for k, v in user_info.items():
                setattr(user.profile, k, v)
            user.profile.save()

            token = issue_token(user)
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
