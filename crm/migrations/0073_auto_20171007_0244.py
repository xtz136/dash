# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-06 18:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0072_auto_20171007_0237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='expired_at',
            field=models.DateField(blank=True, null=True, verbose_name='执照有效日期至'),
        ),
    ]
