# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-12 08:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crm', '0052_item'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemBorrowingRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(blank=True, editable=False, max_length=255, verbose_name='物品名称')),
                ('borrow_date', models.DateTimeField(auto_now_add=True)),
                ('reason', models.CharField(choices=[('办理业务', '办理业务')], default='办理业务', max_length=200)),
                ('status', models.CharField(choices=[('借出中', '借出中'), ('已归还', '已归还'), ('遗失', '遗失')], default='借出中', max_length=200)),
                ('qty', models.PositiveIntegerField(default=1)),
                ('has_returned', models.BooleanField(default=False)),
                ('return_date', models.DateTimeField(blank=True, null=True)),
                ('note', models.TextField(blank=True, verbose_name='备注')),
                ('borrower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterModelOptions(
            name='item',
            options={'verbose_name': '客户资料', 'verbose_name_plural': '客户资料'},
        ),
        migrations.AlterField(
            model_name='item',
            name='borrower',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='借给'),
        ),
        migrations.AlterField(
            model_name='item',
            name='status',
            field=models.CharField(choices=[('寄存', '寄存'), ('借出', '借出'), ('已归还', '已归还'), ('遗失', '遗失')], max_length=200, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='item',
            name='status_updated',
            field=models.DateTimeField(blank=True, editable=False, null=True, verbose_name='状态更新于'),
        ),
        migrations.AddField(
            model_name='itemborrowingrecord',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Item'),
        ),
    ]