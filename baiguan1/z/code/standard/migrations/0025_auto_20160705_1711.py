# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-05 09:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('standard', '0024_auto_20160705_1708'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='standardseries',
            unique_together=set([('vendor_short_name', 'brand', 'series')]),
        ),
    ]
