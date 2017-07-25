# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-25 12:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0020_shareholder_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='custom_entry_no',
            field=models.CharField(blank=True, max_length=255, verbose_name='海关登记编号'),
        ),
        migrations.AddField(
            model_name='company',
            name='custom_expired_at',
            field=models.DateField(blank=True, null=True, verbose_name='有效期'),
        ),
        migrations.AddField(
            model_name='company',
            name='custom_org_code',
            field=models.CharField(blank=True, max_length=255, verbose_name='海关组织机构代码'),
        ),
        migrations.AddField(
            model_name='company',
            name='custom_register_no',
            field=models.CharField(blank=True, max_length=255, verbose_name='海关注册编码'),
        ),
        migrations.AddField(
            model_name='company',
            name='custom_registered_at',
            field=models.DateField(blank=True, null=True, verbose_name='海关登记日期'),
        ),
        migrations.AddField(
            model_name='company',
            name='premise',
            field=models.CharField(blank=True, max_length=255, verbose_name='经营场地（英文)'),
        ),
        migrations.AlterField(
            model_name='shareholder',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Company', verbose_name='公司'),
        ),
        migrations.AlterField(
            model_name='shareholder',
            name='people',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.People', verbose_name='客户'),
        ),
    ]
