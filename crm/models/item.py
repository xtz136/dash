from django.db import models
from django.utils.timezone import now

from django.conf import settings
from crm.models import Company


class Item(models.Model):
    company = models.ForeignKey(Company, verbose_name="公司")
    company_title = models.CharField(
        editable=False, blank=True, max_length=255)
    ITEMS = (
        ("营业执照正本", "营业执照正本"),
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
        ("其它", "其它"),
    )
    item = models.CharField(verbose_name="物品",
                            max_length=200, blank=True, choices=ITEMS)
    qty = models.PositiveIntegerField(verbose_name="数量", default=1)
    STATUS = (
        ('寄存', '寄存'),
        ('借出', '借出'),
        ('已归还', '已归还'),
        ('遗失', '遗失'),

    )
    status = models.CharField(verbose_name="状态",
                              default="寄存",
                              max_length=200, choices=STATUS)
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True, null=True, verbose_name="签收者", related_name="receiver")
    borrower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="借给", blank=True, null=True)
    return_date = models.DateTimeField(
        verbose_name="归还日期", null=True, blank=True)
    created = models.DateTimeField(verbose_name="签收时间", auto_now_add=True)
    status_updated = models.DateTimeField(
        null=True, blank=True, editable=False, verbose_name="状态更新于")
    note = models.CharField(verbose_name="备注", blank=True, max_length=255)

    def __str__(self):
        return '{0} {1}'.format(self.company_title, self.item)

    def borrow_to(self, user):
        """借出"""
        if self.status == "寄存":
            self.borrower = user
            self.set_status("借出")

    def return_back(self):
        """归还"""
        self.borrower = None
        self.return_date = now()
        self.set_status("已归还")

    def set_status(self, status):
        self.status = status
        self.status_updated = now()
        self.save()

    def save(self, *args, **kwargs):
        self.company_title = self.company.title
        super(Item, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "客户资料"
        verbose_name_plural = "客户资料"


class ItemBorrowingRecord(models.Model):
    item = models.ForeignKey(Item, verbose_name="物品")
    item_name = models.CharField(
        verbose_name="物品名称",
        max_length=255, blank=True, editable=False)
    borrow_date = models.DateTimeField(auto_now_add=True, verbose_name="借出日期")
    REASONS = (
        ('办理业务', '办理业务'),
    )
    reason = models.CharField(choices=REASONS,
                              max_length=200,
                              verbose_name="借出事由",
                              default='办理业务')
    STATUS = (
        ('借出中', '借出中'),
        ('已归还', '已归还'),
        ('遗失', '遗失'),
    )
    status = models.CharField(choices=STATUS,
                              max_length=200,
                              default='借出中',
                              verbose_name="状态")
    qty = models.PositiveIntegerField(default=1, verbose_name="数量")
    has_returned = models.BooleanField(
        default=False, verbose_name="是否已归还")
    return_date = models.DateTimeField(
        blank=True, null=True, verbose_name="归还日期")
    note = models.CharField(verbose_name="备注", blank=True, max_length=255)
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 null=True, blank=True,
                                 verbose_name="借用人")
    lender = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="出借者",
        null=True, blank=True, related_name="lender")

    def __str__(self):
        return '{0} {1} {2}'.format(self.item_name, self.borrower, self.status)

    def make_return(self):
        self.status = "已经归还"
        self.return_date = now()
        self.save()

    def save(self, *args, **kwargs):
        self.item_name = self.item.item
        super(ItemBorrowingRecord, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "借出记录"
        verbose_name_plural = "借出记录"
