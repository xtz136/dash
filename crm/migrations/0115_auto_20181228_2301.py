# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-12-28 15:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0114_company_taxpayer'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='food_licence_expired_at',
            field=models.DateField(blank=True, null=True, verbose_name='食品经营许可证有效期'),
        ),
        migrations.AlterField(
            model_name='company',
            name='national_tax_id',
            field=models.CharField(blank=True, max_length=255, verbose_name='税务登记证'),
        ),
        migrations.AlterField(
            model_name='company',
            name='national_tax_office',
            field=models.CharField(blank=True, max_length=255, verbose_name='税务所'),
        ),
        migrations.AlterField(
            model_name='company',
            name='national_tax_phone',
            field=models.CharField(blank=True, max_length=255, verbose_name='税管员电话'),
        ),
        migrations.AlterField(
            model_name='company',
            name='national_tax_staff',
            field=models.CharField(blank=True, max_length=255, verbose_name='税管员'),
        ),
        migrations.AlterField(
            model_name='company',
            name='ss_account',
            field=models.CharField(blank=True, max_length=255, verbose_name='代扣社保账号'),
        ),
        migrations.AlterField(
            model_name='company',
            name='ss_bank',
            field=models.CharField(blank=True, max_length=255, verbose_name='社保开户银行'),
        ),
    ]
