# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-22 08:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('summary', '0015_auto_20160711_2017'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monthlystoreitempattern',
            name='patterns',
        ),
    ]
