# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-13 07:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('summary', '0006_monthlystoreitempattern'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='dailystorecategorysummary',
            unique_together=set([('date', 'store', 'category')]),
        ),
    ]
