# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-13 02:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0085_auto_20171012_0103'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='no',
            field=models.CharField(blank=True, max_length=200, verbose_name='收据编号'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Company', verbose_name='客户'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='时间'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='items',
            field=models.TextField(blank=True, verbose_name='物品列表'),
        ),
    ]