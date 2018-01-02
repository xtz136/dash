import logging
from django.db import models
from django.conf import settings

from crm.models import Company

from django_fsm import FSMField, transition
from core.validators import validate_phone
from core.models import SiteConf
from wechat.utils import send_verify_message

logger = logging.getLogger(__file__)


class Apply(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='用户')
    name = models.CharField('姓名', max_length=200)
    title = models.CharField('公司名称', max_length=200)
    info = models.TextField('其它信息', blank=True)
    phone = models.CharField('电话', max_length=50, validators=[validate_phone])
    company = models.ForeignKey(Company, blank=True, null=True)
    state = FSMField(default='new')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @transition(field=state, source='new', target='approved')
    def approve(self):
        self.user.profile.company = self.company
        self.user.is_active = True
        self.user.save()

        data = {
            'first': {'color': '#173177', 'value': '你的账户已经认证成功！'},
            'keyword1': {'color': '#173177', 'value': self.name},
            'keyword2': {'color': '#173177', 'value': self.phone},
            'keyword3': {'color': '#173177', 'value': self.company.title},
            'keyword4': {'color': '#173177', 'value': self.updated.strftime('%Y-%m-%d')},
            'remark': {'color': '#173177', 'value': '点击消息可以马上查看报表了。'},
        }
        url = 'http://{0}{1}'.format(SiteConf.get_solo().site_address,
                                     reverse('wechat:report-list'))
        try:
            send_verify_message(self.user.access_token.openid, data, url)
        except Exception as e:
            logger.error(e)

    @transition(field=state, source='new', target='denied')
    def deny(self):
        pass
        # send notify

    def save(self, *args, **kwargs):
        instance = super(Apply, self).save(*args, **kwargs)
        if self.company and self.state == 'new':
            self.user.profile.set_name(self.name)
            self.approve()
        return instance

    class Meta:
        ordering = ('-updated', )
        verbose_name = '客户认证申请'
        verbose_name_plural = '客户认证申请'
