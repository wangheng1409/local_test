# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-22 13:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('summary', '0020_auto_20160722_2108'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='monthlystoreitempattern',
            unique_together=set([('date', 'store', 'patterns')]),
        ),
    ]
