# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-22 13:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('summary', '0019_auto_20160722_1643'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='monthlystoreitempattern',
            unique_together=set([]),
        ),
    ]