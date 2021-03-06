from django.db import models


class TaxBureau(models.Model):
    CITYES = (
        ("guangzhou", "广州市"),
        ("zhuhai", "珠海市"),
        ("foshan", "佛山市"),
    )
    city = models.CharField(
        verbose_name="市",
        blank=True,
        choices=CITYES,
        default='guangzhou',
        max_length=200,
    )

    DISTRICTS = (
        ("baiyun", "白云区"),
        ("tianhe", "天河区"),
        ("panyu", "番禺区"),
        ("yuexiu", "越秀区"),
        ("haizhu", "海珠区"),
        ("zengcheng", "增城区"),
        ("nansha", "南沙区"),
        ("conghua", "从化区"),
        ("liwan", "荔湾区"),
        ("huadu", "花都区"),
        ("huangpu", "黄埔区"),
        ("luogang", "萝岗区"),
        ("huadu", "花都区"),
        ("develop", "开发区"),
        ("xiangzhou", "香洲区"),
        ("gongbei", "拱北区"),
        ("other", "其它地区"))

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

    office = models.CharField(
        verbose_name='分局名称',
        blank=True,
        max_length=255)

    address = models.CharField(
        blank=True,
        max_length=255,
        verbose_name="地址")

    full_title = models.CharField(
        blank=True,
        max_length=255,
        verbose_name="全称"
    )

    def __str__(self):
        return self.full_title

    def _full_title(self):
        return "".join(
            self.get_bureau_display(),
            self.get_district_display(),
            self.office)

    class Meta:
        verbose_name = '税局'
        verbose_name_plural = '税局'

    def save(self, *args, **kwargs):
        if not self.full_title:
            self.full_title = self._full_title()
        super(TaxBureau, self).save(*args, **kwargs)
