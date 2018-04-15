from datetime import datetime
from django.db import models
from django.db.models import F

from crm.models import company

from .order import Order


class RevertList(models.Model):

    """归还单
    """

    order_id = models.CharField(verbose_name="编号", max_length=100)
    company = models.ForeignKey(
        company.Company,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="所属公司")
    revert_borrow_date = models.DateField(verbose_name="归还时间")

    @classmethod
    def gen_order_id(cls):
        now = datetime.now()
        date_str = now.strftime('%Y-%m-%d')

        order, _ = Order.objects.get_or_create(date=date_str)
        order.order_id = F('order_id') + 1
        order.save()

        order.refresh_from_db()
        order_id = str(order.order_id).zfill(4)

        return 'YH{}{}'.format(date_str.replace('-', ''), order_id)

    @classmethod
    def create(cls, company_id):
        order_id = cls.gen_order_id()
        now = datetime.now()
        obj = cls(
            order_id=order_id,
            company_id=company_id,
            revert_borrow_date=now)
        obj.save()
        return obj

    class Meta:
        verbose_name = "归还单"
        verbose_name_plural = "归还单"
