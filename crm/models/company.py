from collections import OrderedDict
from datetime import timedelta

from core.models import Attachment
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe
from jsonfield import JSONField
from taggit.managers import TaggableManager

from .tax import TaxBureau

User.add_to_class(
    "__str__",
    lambda u: "{0}{1}".format(u.last_name, u.first_name) if u.last_name else u.username
)


class Company(models.Model):
    title = models.CharField(verbose_name="企业名称", unique=True, max_length=255)
    alias = models.CharField(verbose_name="字号", blank=True, max_length=255)
    tax_username = models.CharField(
        verbose_name="电子税务局用户名", blank=True, max_length=255)
    tax_password = models.CharField(
        verbose_name="电子税务局密码", blank=True, max_length=255)

    TYPES = (('有限责任公司', '有限责任公司'), ('个体工商户', '个体工商户'), ('股份有限公司', '股份有限公司'),
             ('合伙企业(有限合伙)', '合伙企业(有限合伙)'), ('集体所有制(股份合作)', '集体所有制(股份合作)'),
             ('个人独资企业', '个人独资企业'))
    type = models.CharField(
        verbose_name="公司类型", choices=TYPES, default='有限责任公司', max_length=20)
    registered_capital = models.DecimalField(
        help_text="单位 (万元)",
        default=1,
        verbose_name="注册资金",
        max_digits=19,
        decimal_places=2)
    address = models.CharField(verbose_name="地址", blank=True, max_length=255)
    op_address = models.CharField(
        verbose_name="实际经营地址",
        help_text="不填，默认为公司注册地址",
        blank=True,
        max_length=255)

    # 主要业务负责人
    salesman = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="业务员",
        blank=True,
        null=True,
        related_name="customers")
    # 管账人
    bookkeeper = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="记账会计",
        blank=True,
        null=True,
        related_name="accounts")

    taxpayer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="报税会计",
        blank=True,
        null=True,
        related_name="taxpayer")

    # unified social credit code
    uscc = models.CharField(
        verbose_name="社会统一信用代码号", blank=True, max_length=255)

    registered_at = models.DateField(verbose_name="注册日期", blank=True, null=True)
    expired_at = models.DateField(verbose_name="执照有效日期至", blank=True, null=True)
    food_licence_expired_at = models.DateField(
        verbose_name="食品经营许可证有效期", blank=True, null=True)

    business_license = models.CharField(
        verbose_name="营业执照注册号", blank=True, max_length=255)

    INDUSTRIES = [('餐饮', '餐饮'), ('服务业', '服务业'), ('广告', '广告'), ('兼服务业', '兼服务业'),
                  ('建筑', '建筑'), ('零售业', '零售业'), ('贸易', '贸易'), ('租赁业', '租赁业'),
                  ('制造业', '制造业'), ('娱乐', '娱乐'), ('其它', '其它')]
    industry = models.CharField(
        choices=INDUSTRIES, verbose_name="所属行业", default='汽配', max_length=50)

    national_tax_id = models.CharField(
        verbose_name="税务登记证", blank=True, max_length=255)
    # national_tax_sn = models.CharField(
    #     verbose_name="国税编码", blank=True, max_length=255)
    national_tax_staff = models.CharField(
        verbose_name="税管员", blank=True, max_length=255)

    national_tax_office = models.CharField(
        verbose_name='税务所', blank=True, max_length=255)

    BASE_TYPE = [('有', '有'), ('无', '无')]

    national_tax_type = models.CharField(
        verbose_name='国税税种', blank=True, max_length=100, choices=BASE_TYPE)

    individual_tax = models.CharField(
        verbose_name='个税', blank=True, max_length=100, choices=BASE_TYPE)

    stamp_duty = models.CharField(
        verbose_name='印花税', blank=True, max_length=100, choices=BASE_TYPE)

    culture_expenses = models.CharField(
        verbose_name='文化事业费', blank=True, max_length=100, choices=BASE_TYPE)

    sale_tax = models.CharField(
        verbose_name='消费税', blank=True, max_length=100, choices=BASE_TYPE)

    environmental_tax = models.CharField(
        verbose_name="环保税", blank=True, max_length=100, choices=BASE_TYPE)

    ELECTRONIC_INVOICING = BASE_TYPE + [('手撕发票', '手撕发票'), ('区块链', '区块链'), ('网络', '网络')]
    electronic_invoicing = models.CharField(
        verbose_name='电子发票',
        blank=True,
        max_length=100,
        choices=ELECTRONIC_INVOICING)

    quota_month = models.CharField(
        verbose_name="定额(月)", blank=True, max_length=255)

    quota_quarter = models.CharField(
        verbose_name="定额(季)", blank=True, max_length=255)

    national_tax_phone = models.CharField(
        verbose_name="税管员电话", blank=True, max_length=255)

    local_tax_id = models.CharField(
        verbose_name="地税登记证", blank=True, max_length=255)
    local_tax_sn = models.CharField(
        verbose_name="地税编码", blank=True, max_length=255)
    local_tax_staff = models.CharField(
        verbose_name="地税专管员", blank=True, max_length=255)

    local_tax_office = models.CharField(
        verbose_name='地税局', blank=True, max_length=255)
    local_tax_phone = models.CharField(
        verbose_name="地税电话", blank=True, max_length=255)

    taxpayer_bank = models.CharField(
        verbose_name="纳税开户银行", blank=True, max_length=255)
    taxpayer_account = models.CharField(
        verbose_name="纳税账号", blank=True, max_length=255)

    # social security
    ss_bank = models.CharField(
        verbose_name="社保开户银行",
        # help_text="不填，默认为纳税开户行",
        blank=True,
        max_length=255)
    ss_account = models.CharField(
        verbose_name="代扣社保账号",
        # help_text="不填，默认为纳税账号",
        blank=True,
        max_length=255)
    ss_number = models.CharField(
        verbose_name="单位社保号", blank=True, max_length=255)
    ss_date = models.DateField(verbose_name="社保购买时间", blank=True, null=True)
    ss_declared = models.CharField(
        verbose_name="社保申报",
        choices=(
            ("社保", "社保"),
            ("无", "无"),
        ),
        max_length=10,
        blank=True,
        default="无")

    TAX_DISKS = (
        ("无", "无"),
        ("百望", "百望"),
        ("航天", "航天"),
        ("托管(百望)", "托管(百望)"),
        ("托管(航天)", "托管(航天)"),
        ("托管(UK)", "托管(UK)"),
        ("UK", "UK"),
    )
    tax_disk = models.CharField(
        max_length=100,
        default="无",
        verbose_name="税控盘",
        choices=TAX_DISKS,
        blank=True)

    tax_declared_begin = models.DateField(
        verbose_name="税务申报开始时间", blank=True, null=True)
    special_taxes = models.CharField(
        verbose_name="特别税种", blank=True, max_length=255)
    const_tax = models.CharField(verbose_name="定税", blank=True, max_length=255)
    declare_info = models.TextField(
        verbose_name="申报区备注",
        blank=True,
    )
    income_tax = models.CharField(
        verbose_name="所得税", blank=True, max_length=255)
    added_value_tax = models.CharField(
        verbose_name="增值税", blank=True, max_length=255)
    cut_tax = models.CharField(verbose_name="减税", blank=True, max_length=255)
    invoice = models.CharField(verbose_name="代开发票", blank=True, max_length=255)
    batch = models.CharField(
        verbose_name="批量",
        default="",
        blank=True,
        choices=(("批量", "批量"),),
        max_length=100,
    )

    # 个体户
    individual_bank = models.CharField(
        verbose_name='基本户开户银行', blank=True, max_length=255)
    individual_account = models.CharField(
        verbose_name='基本户开账号', blank=True, max_length=255)

    credit_rating = models.CharField(
        verbose_name="信用等级", blank=True, max_length=100)

    RATINGS = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    )
    rating = models.CharField(
        verbose_name='评级', blank=True, max_length=10, choices=RATINGS)

    TAXPAYER_TYPES = [('一般纳税人', '一般纳税人'), ('小规模纳税人', '小规模纳税人')]
    taxpayer_type = models.CharField(
        verbose_name="纳税人类型",
        default='小规模纳税人',
        max_length=10,
        choices=TAXPAYER_TYPES)

    # 海关信息
    custom_register_no = models.CharField(
        verbose_name='海关注册代码', blank=True, max_length=255)

    custom_registered_at = models.DateField(
        verbose_name='海关登记日期', blank=True, null=True)

    custom_expired_at = models.DateField(
        verbose_name="报关有效期", null=True, blank=True)
    has_czk = models.CharField(
        verbose_name="财智卡",
        blank=True,
        choices=(
            ("有", "有"),
            ("无", "无"),
        ),
        max_length=100,
        default="无")
    has_custom_info = models.CharField(
        choices=(
            ("有", "有"),
            ("无", "无"),
        ),
        verbose_name="是否有海关信息",
        max_length=100,
        default="无")

    # 规模
    SCALE_SIZES = [('小型企业', '小型企业'), ('中型企业人)', '中型企业人)'), ('大型企业)', '大型企业)')]
    scale_size = models.CharField(
        verbose_name="规模", default='小型企业', max_length=10, choices=SCALE_SIZES)

    STATUS = [('有效', '有效'), ('无效', '无效'), ('歇业', '歇业'), ('筹备', '筹备')]
    status = models.CharField(
        help_text="无效状态，不再为客户提供服务",
        verbose_name="代理状态",
        default='有效',
        max_length=10,
        choices=STATUS)

    IC_STATUS = [('正常', '正常'), ('经营异常', '经营异常')]
    ic_status = models.CharField(
        help_text="经营异常: 已被工商局列入经营异常名录",
        verbose_name="经营状态",
        default='正常',
        max_length=10,
        choices=IC_STATUS)

    # 附件
    website = models.CharField(verbose_name="公司网站", blank=True, max_length=255)
    note = models.TextField(
        verbose_name="备注", blank=True, help_text='可添加公司的其它备注信息')

    legal_people = models.CharField(
        verbose_name='法人', blank=True, max_length=200)
    legal_phone = models.CharField(
        verbose_name='法人电话', blank=True, max_length=200)

    has_customer_files = models.BooleanField(
        verbose_name='是否有存放客户资料', help_text='详细的资料信息请在备注里添加', default=False)
    shareholder_info = JSONField(
        verbose_name="股东信息",
        default=[],
        null=False,
        editable=False,
    )
    contactor = models.CharField(verbose_name='负责人', max_length=255, blank=True)
    contactor_phone = models.CharField(
        verbose_name='负责人电话', max_length=255, blank=True)
    attachments = GenericRelation(Attachment)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    tag = models.CharField(verbose_name='标签', max_length=100, blank=True)

    LICENSE_STATUS = (('有效', '有效'), ('即将过期', '即将过期'), ('已过期', '已过期'), ('永久有效',
                                                                       '永久有效'))

    license_status = models.CharField(
        max_length=50,
        verbose_name='执照状态',
        blank=True,
        choices=LICENSE_STATUS,
        default='有效')

    def show_shareholder_info(self):
        t = ''.join([
            '<li>{role} {name} {phone}</li>'.format(**o)
            for o in self.shareholder_info
        ])
        return mark_safe('<ul>{0}</ul>'.format(t))

    show_shareholder_info.short_description = '股东信息'

    def show_contactor_info(self):
        return mark_safe('{0} {1}'.format(self.contactor, self.contactor_phone))

    show_contactor_info.short_description = '联系人信息'

    def __str__(self):
        return self.title

    def check_expired(self):
        if not self.expired_at:
            self.license_status = '永久有效'
        elif self.expired_at <= timezone.now().date():
            self.license_status = '已过期'
        elif self.expired_at <= timezone.now().date() + timedelta(days=30):
            self.license_status = '即将过期'
        return self.license_status

    def save(self, *args, **kwargs):
        self.title = self.title.strip()
        if not self.op_address:
            self.op_address = self.address

        if not self.ss_bank:
            self.ss_bank = self.taxpayer_bank

        if not self.ss_account:
            self.ss_account = self.taxpayer_account

        if not self.legal_people:
            try:
                self.legal_people = self.shareholder_set.get(
                    role='法人').people.name
            except:
                pass
        self.check_expired()
        return super(Company, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "公司"
        verbose_name_plural = "公司"
