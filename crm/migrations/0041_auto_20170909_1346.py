# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-09 05:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0040_remove_company_national_tax_sn'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='alias',
            field=models.CharField(blank=True, max_length=255, verbose_name='字号'),
        ),
        migrations.AddField(
            model_name='company',
            name='tax_bureau_password',
            field=models.CharField(blank=True, max_length=255, verbose_name='电子税务局密码'),
        ),
        migrations.AddField(
            model_name='company',
            name='tax_bureau_username',
            field=models.CharField(blank=True, max_length=255, verbose_name='电子税务局用户名'),
        ),
    ]
