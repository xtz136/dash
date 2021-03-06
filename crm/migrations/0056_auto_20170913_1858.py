# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-13 10:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0055_auto_20170913_0431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='bookkeeper',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='accounts', to=settings.AUTH_USER_MODEL, verbose_name='记账会计'),
        ),
        migrations.AlterField(
            model_name='company',
            name='local_tax_office',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='local_taxes', to='crm.TaxBureau', verbose_name='地税所属分局'),
        ),
        migrations.AlterField(
            model_name='company',
            name='national_tax_office',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='national_taxes', to='crm.TaxBureau', verbose_name='国税所属分局'),
        ),
        migrations.AlterField(
            model_name='company',
            name='salesman',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customers', to=settings.AUTH_USER_MODEL, verbose_name='业务员'),
        ),
        migrations.AlterField(
            model_name='itemborrowingrecord',
            name='note',
            field=models.CharField(blank=True, max_length=255, verbose_name='备注'),
        ),
    ]
