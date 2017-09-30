# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-21 07:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0065_auto_20170915_1926'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='bookkeeper_username',
            field=models.CharField(blank=True, editable=False, max_length=200, verbose_name='记账员'),
        ),
        migrations.AddField(
            model_name='company',
            name='salesman_username',
            field=models.CharField(blank=True, editable=False, max_length=200, verbose_name='业务员'),
        ),
    ]
