# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-23 04:47
from __future__ import unicode_literals

import datetime
import django.contrib.postgres.fields
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('standard', '0006_standarditem_keywords'),
    ]

    operations = [
        migrations.AddField(
            model_name='standarditem',
            name='alias',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), null=True, size=None, verbose_name='\u522b\u540d'),
        ),
        migrations.AddField(
            model_name='standarditem',
            name='last_updated',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 6, 23, 4, 47, 45, 140808, tzinfo=utc), verbose_name='\u6700\u540e\u66f4\u65b0\u65f6\u95f4'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='standarditem',
            name='num_matches',
            field=models.PositiveIntegerField(default=0, verbose_name='\u5339\u914d\u5546\u54c1\u6570'),
        ),
    ]
