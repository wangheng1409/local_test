# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-21 05:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('standard', '0004_auto_20160621_1122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='standarditem',
            name='keywords',
        ),
    ]
