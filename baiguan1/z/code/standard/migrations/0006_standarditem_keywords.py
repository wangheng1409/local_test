# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-21 05:47
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('standard', '0005_remove_standarditem_keywords'),
    ]

    operations = [
        migrations.AddField(
            model_name='standarditem',
            name='keywords',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), null=True, size=None, verbose_name='\u5173\u952e\u8bcd'),
        ),
    ]