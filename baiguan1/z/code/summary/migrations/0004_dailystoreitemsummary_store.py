# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-31 09:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20160531_1731'),
        ('summary', '0003_auto_20160531_1602'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailystoreitemsummary',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_summary', to='store.Store', verbose_name='\u5546\u5e97'),
        ),
    ]
