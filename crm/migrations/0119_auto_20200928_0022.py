# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2020-09-27 16:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0118_auto_20200430_0028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='electronic_invoicing',
            field=models.CharField(blank=True, choices=[('有', '有'), ('无', '无'), ('手撕发票', '手撕发票'), ('区块链', '区块链'), ('网络', '网络')], max_length=100, verbose_name='电子发票'),
        ),
        migrations.AlterField(
            model_name='company',
            name='tax_disk',
            field=models.CharField(blank=True, choices=[('无', '无'), ('百望', '百望'), ('航天', '航天'), ('托管(百望)', '托管(百望)'), ('托管(航天)', '托管(航天)'), ('托管(uk)', '托管(uk)'), ('UK', 'UK')], default='无', max_length=100, verbose_name='税控盘'),
        ),
    ]