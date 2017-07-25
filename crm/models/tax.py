from django.db import models


class TaxBureau(models.Model):
    DISTRICTS = (
        ("baiyun", "白云区"), ("tianhe", "天河区"), ("panyu", "番禺区"),
        ("yuexiu", "越秀区"), ("haizhu", "海珠区"), ("zengcheng", "增城区"),
        ("huadu", "花都区"), ("other", "其它地区"))

    district = models.CharField(
        verbose_name="所属区",
        choices=DISTRICTS,
        blank=True,
        max_length=50)

    BUREAUS = (
        ('national', '国税局'),
        ('local', '地税局'))

    bureau = models.CharField(
        verbose_name="税局",
        choices=BUREAUS,
        blank=True,
        max_length=50)

    address = models.CharField(
        blank=True,
        max_length=255,
        verbose_name="地址")

    def __str__(self):
        return "{0} {1}".format(self.district, self.bureau)

    class Meta:
        verbose_name = '税局'
        verbose_name_plural = '税局'
