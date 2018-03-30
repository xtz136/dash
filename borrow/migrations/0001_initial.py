# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-03-29 14:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crm', '0111_auto_20180328_1621'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='name')),
                ('descript', models.CharField(blank=True, max_length=100, verbose_name='descript')),
            ],
            options={
                'verbose_name': '物品',
                'verbose_name_plural': '物品',
            },
        ),
        migrations.CreateModel(
            name='EntityList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0, verbose_name='数量')),
                ('sign_date', models.DateField(blank=True, null=True, verbose_name='签收日期')),
                ('borrow_date', models.DateField(blank=True, null=True, verbose_name='借用日期')),
                ('revert_borrow_date', models.DateField(blank=True, null=True, verbose_name='还回日期')),
                ('revert_date', models.DateField(blank=True, null=True, verbose_name='归还日期')),
                ('status', models.CharField(choices=[('寄存', '寄存'), ('借出', '借出'), ('归还', '归还')], default='寄存', max_length=100, verbose_name='状态')),
                ('descript', models.CharField(blank=True, max_length=255, verbose_name='备注')),
                ('borrower', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='borrower_user', to=settings.AUTH_USER_MODEL, verbose_name='借用人')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='crm.Company', verbose_name='所属公司')),
                ('entity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='borrow.Entity', verbose_name='物品名称')),
                ('signer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='signer_user', to=settings.AUTH_USER_MODEL, verbose_name='签收人')),
            ],
            options={
                'verbose_name': '物品清单',
                'verbose_name_plural': '物品清单',
            },
        ),
    ]
