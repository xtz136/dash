# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-04 16:02
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0026_auto_20171204_2253'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='privacies',
            field=jsonfield.fields.JSONField(default=[]),
        ),
        migrations.AddField(
            model_name='file',
            name='privacy_on',
            field=models.BooleanField(default=False),
        ),
    ]
