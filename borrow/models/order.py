from django.db import models


class Order(models.Model):

    """每一次归还资料，都会生产一个订单，这个表主要是为了保存订单编号
    每天重新计算订单编号
    """

    order_id = models.IntegerField(verbose_name="编号", default=1)
    date = models.DateField(verbose_name="时间")
