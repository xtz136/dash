# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-25 13:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0024_auto_20170725_2052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='local_tax_branch',
        ),
        migrations.AddField(
            model_name='company',
            name='local_tax_office',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='local_taxes', to='crm.TaxBureau', verbose_name='地税所属分局'),
        ),
        migrations.AlterField(
            model_name='company',
            name='national_tax_office',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='national_taxes', to='crm.TaxBureau', verbose_name='国税所属分局'),
        ),
    ]
