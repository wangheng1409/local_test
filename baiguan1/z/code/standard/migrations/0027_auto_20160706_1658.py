# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-06 08:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('standard', '0026_standardcompany'),
    ]

    operations = [
        migrations.AlterField(
            model_name='standardcompany',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='\u4f01\u4e1a\u7b80\u79f0'),
        ),
        migrations.AlterField(
            model_name='standardcompany',
            name='num_na',
            field=models.PositiveIntegerField(default=0, verbose_name='\u4e0d\u5904\u7406\u6570'),
        ),
    ]