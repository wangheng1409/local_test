# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-04 04:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('standard', '0018_auto_20160704_1222'),
    ]

    operations = [
        migrations.RenameField(
            model_name='standarditem',
            old_name='short_vendor_name',
            new_name='vendor_short_name',
        ),
    ]
