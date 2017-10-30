# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-02 11:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('standard', '0012_standardvendor'),
    ]

    operations = [
        migrations.AddField(
            model_name='standardvendor',
            name='status',
            field=models.CharField(choices=[(b'pending_review', '\u5f85\u5ba1\u6838'), (b'human_verified', '\u5df2\u901a\u8fc7\u4eba\u5de5\u5ba1\u6838')], default=b'pending_review', max_length=100, verbose_name='\u72b6\u6001'),
        ),
    ]
