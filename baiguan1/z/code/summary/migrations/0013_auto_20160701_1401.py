# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-01 06:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summary', '0012_auto_20160625_2103'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailystoreitemsummary',
            name='unit_price',
            field=models.FloatField(blank=True, null=True, verbose_name='\u552e\u4ef7'),
        ),
        migrations.AddField(
            model_name='monthlystoreitemsummary',
            name='unit_price',
            field=models.FloatField(blank=True, null=True, verbose_name='\u552e\u4ef7'),
        ),
    ]
