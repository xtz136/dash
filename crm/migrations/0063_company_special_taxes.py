# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-15 09:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0062_auto_20170915_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='special_taxes',
            field=models.CharField(blank=True, max_length=255, verbose_name='特别税种'),
        ),
    ]
