# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-19 15:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0032_auto_20171215_0104'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='size',
            field=models.BigIntegerField(default=0),
        ),
    ]
