# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-28 08:54
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('standard', '0033_standardtag_alias'),
    ]

    operations = [
        migrations.AddField(
            model_name='standardtag',
            name='created_at',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2016, 9, 28, 8, 54, 44, 3781, tzinfo=utc), verbose_name='\u751f\u6210\u65e5\u671f'),
            preserve_default=False,
        ),
    ]
