# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-05 17:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0009_profile_sex'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Profile',
            new_name='ProfileOld',
        ),
    ]
