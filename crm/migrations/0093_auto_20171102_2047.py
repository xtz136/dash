# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-02 12:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0092_auto_20171030_2359'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='legal_people_phone',
            field=models.CharField(blank=True, max_length=200, verbose_name='法人电话'),
        ),
        migrations.AlterField(
            model_name='company',
            name='business_license',
            field=models.CharField(blank=True, max_length=255, verbose_name='营业执照注册号'),
        ),
        migrations.AlterField(
            model_name='company',
            name='contactor_phone',
            field=models.CharField(blank=True, max_length=255, verbose_name='负责人联系电话'),
        ),
        migrations.AlterField(
            model_name='company',
            name='industry',
            field=models.CharField(choices=[('汽配', '汽配'), ('餐饮', '餐饮'), ('服装', '服装'), ('批发业', '批发业'), ('建筑', '建筑'), ('商贸', '商贸'), ('广告', '广告'), ('房地产', '房地产'), ('服务业', '服务业'), ('贸易', '贸易'), ('娱乐', '娱乐'), ('其它', '其它')], default='汽配', max_length=50, verbose_name='所属行业'),
        ),
        migrations.AlterField(
            model_name='shareholder',
            name='share',
            field=models.FloatField(default=0.1, verbose_name='股份占比%'),
        ),
    ]
