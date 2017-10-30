# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-11 07:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_auto_20160711_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='complete_rate',
            field=models.FloatField(default=0, verbose_name='\u5b8c\u6210\u5ea6'),
        ),
        migrations.AlterField(
            model_name='store',
            name='num_na',
            field=models.PositiveIntegerField(default=0, verbose_name='\u4e0d\u5904\u7406\u5546\u54c1\u6570'),
        ),
        migrations.AlterField(
            model_name='store',
            name='num_new_items',
            field=models.PositiveIntegerField(default=0, verbose_name='\u65b0\u54c1\u6570'),
        ),
        migrations.AlterField(
            model_name='store',
            name='num_pending_items',
            field=models.PositiveIntegerField(default=0, verbose_name='\u5f85\u5ba1\u6838\u5546\u54c1\u6570'),
        ),
        migrations.AlterField(
            model_name='store',
            name='num_sku',
            field=models.PositiveIntegerField(default=0, verbose_name='SKU'),
        ),
        migrations.AlterField(
            model_name='store',
            name='num_verified_items',
            field=models.PositiveIntegerField(default=0, verbose_name='\u6807\u54c1\u6570'),
        ),
    ]
