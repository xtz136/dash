# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-30 09:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0090_auto_20171030_1726'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='premise',
        ),
        migrations.AlterField(
            model_name='company',
            name='credit_rating',
            field=models.CharField(blank=True, max_length=100, verbose_name='信用等级'),
        ),
        migrations.AlterField(
            model_name='company',
            name='has_czk',
            field=models.CharField(blank=True, choices=[('有', '有'), ('无', '无')], default='无', max_length=100, verbose_name='有财智卡'),
        ),
    ]
