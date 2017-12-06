from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from django_fsm import FSMField, transition
from notifications.signals import notify
from crm.models import Company


class MemberApplication(models.Model):
    applicant = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='applicant')
    mobile = models.CharField('手机号码', max_length=100, blank=True)
    job_title = models.CharField('职位', max_length=100, blank=True)
    company_title = models.CharField('公司名称', max_length=255, blank=True)
    company = models.ForeignKey(Company, blank=True, null=True)
    info = models.TextField('其它信息', blank=True)
    reason = models.TextField('拒绝理由', blank=True)
    auditor = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='auditor', null=True, blank=True)
    state = FSMField(default='new')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0} - {1}'.format(self.company_title, self.applicant)

    def has_auditor(self):
        return self.auditor is not None

    def has_company_assoc(self):
        return self.company is not None and self.auditor is not None

    def can_approve(self):
        return self.has_auditor() and self.has_company_assoc()

    @transition(field=state, source='new', target='approved',
                conditions=[can_approve])
    def approved(self):
        notify.send(self.auditor, recipient=self.applicant, verb='审核通过')

    @transition(field=state, source='new', target='denied',
                conditions=[has_auditor])
    def denied(self):
        notify.send(self.auditor, recipient=self.applicant,
                    verb='拒绝', description=self.reason)


@receiver(post_save, sender=MemberApplication)
def handle_new(sender, instance, created, **kwargs):
    if created:
        User = get_user_model()
        users = User.objects.filter(is_superuser=True)
        notify.send(instance.applicant, recipient=users, verb='申请开通账号')
