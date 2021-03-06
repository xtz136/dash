# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-20 17:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_application'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='company_title',
        ),
        migrations.AddField(
            model_name='application',
            name='title',
            field=models.CharField(blank=True, max_length=200, verbose_name='company title'),
        ),
        migrations.AlterField(
            model_name='application',
            name='name',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='application',
            name='phone',
            field=models.CharField(blank=True, max_length=50, verbose_name='phone'),
        ),
    ]
