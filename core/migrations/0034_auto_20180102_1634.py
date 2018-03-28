# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-01-02 08:34
from __future__ import unicode_literals

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_auto_20171228_1833'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteconf',
            name='wx_report_tpl',
            field=models.TextField(blank=True, verbose_name='微信报表通知模板'),
        ),
        migrations.AlterField(
            model_name='apply',
            name='phone',
            field=models.CharField(max_length=50, validators=[core.validators.validate_phone], verbose_name='电话'),
        ),
    ]
