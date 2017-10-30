from random import randint
import json
from collections import OrderedDict
from django.core import serializers

from django.db import models
from django.utils.timezone import now
from django.conf import settings
from jsonfield import JSONField

from crm.models import Company


class Receipt(models.Model):
    """签收/归还收据"""
    TYPES = (
        ('签收', '签收'),
        ('归还', '归还'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="操作员")
    company = models.ForeignKey(
        Company, blank=True, null=True, verbose_name='客户')
    created = models.DateTimeField(verbose_name="时间", default=now)
    type = models.CharField(
        verbose_name="类型", choices=TYPES, default="签收", max_length=50)
    items = models.TextField(verbose_name="物品列表", blank=True)
    no = models.CharField(verbose_name="收据编号", max_length=200, blank=True)

    @classmethod
    def create_receipt(cls, **kwargs):
        items = kwargs.pop('items', [])
        return cls.objects.create(items=serializers.serialize('json', items),
                                  **kwargs)

    def get_items(self):
        return serializers.deserialize('json', self.items)

    @property
    def count(self):
        return sum(i.object.qty for i in self.get_items())

    def save(self, *args, **kwargs):
        if not self.no:
            self.no = 'YH{0}{1}'.format(
                self.created.strftime('%Y%m%d'), self._randno())
        super(Receipt, self).save(*args, **kwargs)

    def _randno(self):
        return ''.join(map(str, [randint(0, 9) for i in range(4)]))


class Item(models.Model):
    TYPES = (("营业执照正本", "营业执照正本"),
             ("营业执照副本", "营业执照副本"),
             ("金税盘", "金税盘"),
             ("发票领购本", "发票领购本"),
             ("公章", "公章"),
             ("发票章", "发票章"),
             ("财务章", "财务章"),
             ("私章", "私章"),
             ("公司章程", "公司章程"),
             ("扣款协议", "扣款协议"),
             ("开户许可证", "开户许可证"),
             ("机构信用代码证", "机构信用代码证"),
             ("身份证原件", "身份证原件"),
             ("开业通知书", "开业通知书"),
             ("变更通知书", "变更通知书"),
             ("账册", "账册"),
             ("凭证", "凭证"),
             ("租赁合同", "租赁合同"),
             ("汇缴报告", "汇缴报告"),
             ("其它", "其它"))

    company = models.ForeignKey(Company,
                                verbose_name='所属客户',
                                blank=True, null=True)
    company_title = models.CharField(
        verbose_name="公司名称",
        max_length=255, editable=False, blank=True)
    name = models.CharField(verbose_name="物品名", max_length=255)
    qty = models.PositiveIntegerField(default=1, verbose_name="数量")
    type = models.CharField(verbose_name="类型",
                            default="身份证原件",
                            choices=TYPES,
                            max_length=100)
    STATUS = (
        ('寄存', '寄存'),
        ('借出', '借出'),
        ('已归还', '已归还'),
        ('遗失', '遗失'),
        ('损坏', '损坏'),
    )
    status = models.CharField(verbose_name="状态",
                              default="寄存",
                              max_length=50,
                              choices=STATUS)

    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True, null=True,
        verbose_name="签收者",
        related_name="receiver")
    borrower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="借用人",
        blank=True,
        null=True,
        related_name='borrower')

    return_date = models.DateTimeField(
        verbose_name="归还日期", null=True, blank=True)
    received_at = models.DateTimeField(
        verbose_name="签收日期", blank=True, null=True)
    status_updated = models.DateTimeField(
        null=True, blank=True, editable=False, verbose_name="状态更新于")
    note = models.CharField(verbose_name="备注", blank=True, max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.company:
            self.company_title = self.company.title
        if not self.received_at:
            self.received_at = self.created
        super(Item, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-created', )


class Log(models.Model):
    """借出/归还/签收记录"""
    # TODO: 是否需要记录操作员?
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    item = models.ForeignKey(Item)
    qty = models.PositiveIntegerField()
    action = models.CharField(blank=True, max_length=100)
    info = models.CharField(verbose_name='备注', blank=True, max_length=255)
    created = models.DateTimeField(auto_now_add=True)
