# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-04 04:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('standard', '0017_auto_20160704_1042'),
    ]

    operations = [
        migrations.AddField(
            model_name='standarditem',
            name='short_vendor_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='\u4f01\u4e1a\u7b80\u79f0'),
        ),
        migrations.AlterField(
            model_name='standarditem',
            name='vendor',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='\u751f\u7522\u5382\u5546'),
        ),
        migrations.AlterField(
            model_name='standardvendor',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='\u751f\u7522\u5382\u5546'),
        ),
        migrations.AlterField(
            model_name='standardvendor',
            name='standard_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='\u4f01\u4e1a\u7b80\u79f0'),
        ),
    ]
