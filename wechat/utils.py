from datetime import datetime

from rest_framework_jwt.settings import api_settings
from wechatpy import WeChatClient

from core.models import SiteConf

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def issue_token(user):
    payload = jwt_payload_handler(user)
    return {
        'token': jwt_encode_handler(payload),
        'user': user
    }


def validate_month(s):
    try:
        return datetime.strptime(s, '%Y-%m')
    except Exception:
        return None


def get_wechat_client():
    instance = SiteConf.get_solo()
    return WeChatClient(instance.wx_appid, instance.wx_appsecret)


def send_report_message(openid, data, url=None, **kwargs):
    """发送报表模板消息"""
    conf = SiteConf.get_solo()
    client = get_wechat_client()
    tid = conf.wx_tpl_report
    client.message.send_template(openid, tid, data, url, **kwargs)


def send_verify_message(openid, data, url=None, **kwargs):
    """发送绑定用户通知模板消息"""
    conf = SiteConf.get_solo()
    client = get_wechat_client()
    tid = conf.wx_tpl_verify
    client.message.send_template(openid, tid, data, url, **kwargs)
