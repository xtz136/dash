import logging
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.timezone import now
from django.contrib.contenttypes.fields import GenericRelation

from jsonfield.fields import JSONField

from core.models import Attachment, SiteConf
from crm.models import Company
from wechat.utils import send_report_message

logger = logging.getLogger(__file__)


class Report(models.Model):
    """记账结果"""

    company = models.ForeignKey(Company, verbose_name='公司')
    bookkeeper = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='记账员')
    date = models.DateField(default=now, verbose_name='日期')
    data = JSONField(default='{}', blank=True)

    attachments = GenericRelation(Attachment)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('company', 'date')
        ordering = ('-date', 'company')
        verbose_name = '查报表'
        verbose_name_plural = '查报表'

    def __str__(self):
        return 'Report_{0}_{1}'.format(
            self.company.title,
            self.date.strftime('%Y%m'))

    def save(self, *args, **kwargs):
        return super(Report, self).save(*args, **kwargs)

    def get_subscribers(self):
        # TODO : too complex query
        return [p.user for p in self.company.profile_set.all()]

    def send_message(self):
        month = self.date.strftime('%Y-%m')
        url = '{0}{1}?month={2}'.format(SiteConf.get_site_url(),
                                        reverse('wechat:report-list'),
                                        month)

        data = {
            'first': {'color': '#173177', 'value': '你好，贵公司记账报税服务已经完成。'.format(month)},
            'keyword1': {'color': '#173177', 'value': self.company.title},
            'keyword2': {'color': '#173177', 'value': month},
            'keyword3': {'color': '#173177', 'value': month},
            'remark': {'color': '#173177', 'value': '点击消息可以马上查看报表了。'},
        }

        for user in self.get_subscribers():
            try:
                openid = user.access_token.openid
                send_report_message(openid, data, url)
            except Exception as e:
                logger.error(e)
