# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-11-06 06:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0054_auto_20161106_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribute',
            name='foreign_id',
            field=models.CharField(db_index=True, max_length=100, null=True, verbose_name='\u5bf9\u65b9\u6570\u636e\u5e93id'),
        ),
    ]
