# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-16 03:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('standard', '0030_standardcompany_vector'),
        ('store', '0025_auto_20160716_1113'),
    ]

    operations = [
        migrations.AddField(
            model_name='storeitem',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='store_items', to='standard.StandardCompany', verbose_name='\u54c1\u724c'),
        ),
    ]
