# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-09 03:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('standard', '0035_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='standarditem',
            name='source',
            field=models.CharField(choices=[(b'barcode_store', '\u6761\u7801\u5e97'), (b'food_safety', '\u98df\u54c1\u5b89\u5168\u5b98\u7f51')], default=b'barcode_store', max_length=100, verbose_name='\u4f86\u6e90'),
        ),
    ]
