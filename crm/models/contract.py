from django.contrib.auth.models import User
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.utils import timezone

from .company import Company
from core.models import Attachment


class Contract(models.Model):
    title = models.CharField(verbose_name="合同抬头", max_length=255)
    content = models.TextField(verbose_name="合同内容", blank=True)
    company = models.ForeignKey(
        Company, verbose_name="公司", related_name="contracts")
    salesman = models.ForeignKey(
        User, verbose_name="业务员", related_name="contracts")

    CONTRACT_TYPES = (
        ('tax', '报税服务'),
    )

    type = models.CharField(
        verbose_name="合同类型", choices=CONTRACT_TYPES, max_length=10
    )

    SUBSCRIPTION_TYPES = (
        ('onetime', '一次性结算'),
        ('month', '按月结算'),
        ('season', '按季度结算'),
        ('year', '按年结算'),
    )
    subscription_type = models.CharField(
        verbose_name='结算类型', choices=SUBSCRIPTION_TYPES, max_length=10)
    duration = models.PositiveIntegerField(
        verbose_name="服务期", help_text='选择结算类型，自动按一次性/月/季度/年结算', default=3)

    created = models.DateField(verbose_name="创建日期", default=timezone.now)
    expired_at = models.DateField(verbose_name="到期日期")
    amount = models.DecimalField(
        verbose_name="合同金额", max_digits=20, decimal_places=2)
    receivables = models.DecimalField(
        verbose_name="应收款项", max_digits=20, decimal_places=2)
    received = models.DecimalField(
        verbose_name="已收款项", max_digits=20, decimal_places=2, default=0)
    arrearage = models.DecimalField(
        verbose_name="欠款", max_digits=20, decimal_places=2, default=0)

    STATUS = (
        ('draft', '草稿'),
        ('review', '审核中'),
        ('approved', '审核通过'),
        ('perform', '执行中'),
        ('suspend', '暂停'),
        ('expired', '到期'),
        ('halted', '终止')
    )
    status = models.CharField(
        verbose_name="合同状态", default='draft', max_length=10, choices=STATUS)

    updated = models.DateTimeField(auto_now=True)
    company_title = models.CharField(
        verbose_name="公司抬头",
        editable=False,  max_length=255)
    salesman_name = models.CharField(
        verbose_name="业务员",
        editable=False, max_length=100)
    attachments = GenericRelation(Attachment)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.company_title = self.company.title
        self.salesman_name = self.salesman.username
        if not self.receivables:
            self.receivables = self.amount
        return super(Contract, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "合同"
        verbose_name_plural = "合同"
