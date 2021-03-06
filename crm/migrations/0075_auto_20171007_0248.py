# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-06 18:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0074_auto_20171007_0247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='license_status',
            field=models.CharField(blank=True, choices=[('有效', '有效'), ('即将过期', '即将过期'), ('已过期', '已过期'), ('永久有效', '永久有效')], default='有效', editable=False, max_length=50, verbose_name='执照状态'),
        ),
    ]
