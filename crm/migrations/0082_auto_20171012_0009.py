# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-11 16:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0081_item_company_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receipt',
            name='date',
        ),
        migrations.AddField(
            model_name='receipt',
            name='received_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='日期'),
        ),
    ]