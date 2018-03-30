from django.db import models
from crm.models import company, people
from django.contrib.auth.models import User
from .entity import Entity


class EntityList(models.Model):

    """代表了实体清单
    Args:
        company(Company): 关联某个公司
        entity(Entity): 关联某个实体
        amount(int): 数量
        signer(People): 关联某个用户，签收人
        sign_date(Date): 签收日期
        borrower(People): 关联某个用户，借用人
        borrow_date(Date): 借用日期
        revert_borrow_date(Data): 还回日期
        revert_date(Date): 归还日期
        status(str): 状态
        descript(str): 备注
    """

    company = models.ForeignKey(
        company.Company,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="所属公司")

    entity = models.ForeignKey(
        Entity,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="物品名称")

    amount = models.IntegerField(verbose_name="数量", default=0)

    signer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="签收人",
        related_name="signer_user",
        blank=True,
        null=True)

    sign_date = models.DateField(verbose_name="签收日期", blank=True, null=True)

    borrower = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="借用人",
        related_name="borrower_user",
        blank=True,
        null=True)

    borrow_date = models.DateField(verbose_name="借用日期", blank=True, null=True)

    revert_borrow_date = models.DateField(
        verbose_name="还回日期", blank=True, null=True)

    revert_date = models.DateField(verbose_name="归还日期", blank=True, null=True)

    status = models.CharField(
        verbose_name="状态", default="寄存", max_length=100, choices=(
            ('寄存', '寄存'), ('借出', '借出'), ('归还', '归还')))

    descript = models.CharField(verbose_name="备注", max_length=255, blank=True)

    def __str__(self):
        return '{}-{}'.format(self.company, self.entity)

    class Meta:
        verbose_name = "物品清单"
        verbose_name_plural = "物品清单"
