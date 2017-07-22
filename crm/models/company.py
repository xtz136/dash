from django.contrib.auth.models import User
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from core.models import Attachment


class Company(models.Model):
    title = models.CharField(name="企业名称", blank=True, max_length=255)
    registered_capital = models.DecimalField(
        name="注册资金", max_digits=20, decimal_places=0)
    address = models.CharField(name="地址", blank=True, max_length=255)

    saleman = models.ForeignKey(
        User, name="业务员", blank=True, null=True, related_name="salesmen")
    bookkeeper = models.ForeignKey(
        User, name="记账会计", blank=True, null=True, related_name="bookkeeps")

    # unified social credit code
    uscc = models.CharField(name="社会统一信用代码号", blank=True, max_length=255)

    registered_at = models.DateField(name="注册日期", blank=True)
    expired_at = models.DateField(name="执照有效日期", blank=True)

    business_license = models.CharField(
        name="营业执照号", blank=True, max_length=255)

    INDUSTRIES = (('auto_parts', '汽配'), ('food', '餐饮'), ('clother', '服装'),
                  ('ad', '广告'), ('property', '房地产'), ('service', '服务业'),
                  ('trade', '贸易'), ('entertainment', '娱乐'))
    industry = models.CharField(
        choices=INDUSTIES, name="所属行业", default='auto_parts', max_length=50)

    BRANCHES = (("baiyun", "白云区"), ("tianhe", "天河区"), ("panyu", "番禺区"),
                ("yuexiu", "越秀区"), ("haizhu", "海珠区"), ("zengcheng", "增城区"),
                ("huadu", "花都区"), ("other", "其它地区"))

    national_tax_id = models.CharField(name="国税登记证", blank=True, max_length=255)
    national_tax_sn = models.CharField(name="国税编码", blank=True, max_length=255)
    national_tax_staff = models.CharField(
        name="国税专管员", blank=True, max_length=255)
    national_tax_branch = models.CharField(
        choices=BRANCHES, name="国税所属分局", blank=True, max_length=10)
    national_tax_phone = models.CharField(name="电话", blank=True, max_length=255)

    local_tax_id = models.CharField(name="地税登记证", blank=True, max_length=255)
    local_tax_sn = models.CharField(name="地税编码", blank=True, max_length=255)
    local_tax_staff = models.CharField(name="地税专管员", blank=True, max_length=255)
    local_tax_branch = models.CharField(
        choices=BRANCHES, name="地税所属分局", blank=True, max_length=10)
    local_tax_phone = models.CharField(name="电话", blank=True, max_length=255)

    taxpayer_bank = models.CharField(name="纳税开户银行", blank=True, max_length=255)
    taxpayer_account = models.CharField(name="纳税账号", blank=True, max_length=255)

    # social security
    ss_bank = models.CharField(
        name="社保开户银行", help_text="不填，默认为纳税开户行", blank=True, max_length=255)
    ss_account = models.CharField(
        name="代扣社保账号", help_text="不填，默认为纳税账号", blank=True, max_length=255)
    ss_number = models.CharField(name="单位社保号", blank=True, max_length=255)

    CREDIT_RATINGS = (('good', '良好'), ('bad', '差'), ('very_bad', '很差'),)
    credit_rating = models.CharField(
        name="信用评级", default='good', max_length=10, choices=CREDIT_RATINGS)

    STATUS = (('normal', '正常'), ('suspend', '暂停'), ('halted', '终止'))
    status = models.CharField(
        name="公司状态", default='normal', max_length=10, choices=STATUS)
    # 附件
    website = models.CharField(name="公司网站", blank=True, max_length=255)

    attachments = GenericRelation(Attachment)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.ss_bank:
            self.ss_bank = self.taxpayer_bank
        if not self.ss_account:
            self.ss_account = self.taxpayer_account
        super(Company, self).save(*args, **kwargs)