# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-22 08:42
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summary', '0017_monthlystoreitempattern_patterns'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthlystoreitempattern',
            name='patterns',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), null=True, size=None, verbose_name='\u5546\u54c1\u540d'),
        ),
    ]