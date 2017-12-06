from django.db import models
from django.conf import settings

from django_fsm import FSMField, transition
from crm.models import Company


class MemberApplication(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    mobile = models.CharField('手机号码', max_length=100, blank=True)
    job_title = models.CharField('职位', max_length=100, blank=True)
    company_title = models.CharField('公司名称', max_length=255, blank=True)
    company = models.ForeignKey(Company, blank=True, null=True)
    info = models.TextField('其它信息', blank=True)
    reason = models.TextField('拒绝理由', blank=True)
    state = FSMField(default='new')

    def __str__(self):
        return '{0} - {1}'.format(self.company_title, self.user)

    def can_approve(self):
        return self.company is not None

    @transition(field=state, source='new', target='approved', conditions=[can_approve])
    def approved(self):
        pass

    @transition(field=state, source='new', target='denied')
    def denied(self):
        pass
