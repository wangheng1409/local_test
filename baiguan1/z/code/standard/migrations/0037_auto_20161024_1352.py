# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-24 05:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('standard', '0036_standarditem_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='standardtag',
            name='type',
            field=models.CharField(choices=[(b'brand', '\u54c1\u724c'), (b'series', '\u7cfb\u5217'), (b'category', '\u5546\u54c1\u5206\u7c7b'), (b'property', '\u5546\u54c1\u5c5e\u6027'), (b'quantity', '\u5546\u54c1\u6570\u91cf'), (b'ignore', '\u5ffd\u7565')], max_length=100, verbose_name='\u7c7b\u522b'),
        ),
    ]
