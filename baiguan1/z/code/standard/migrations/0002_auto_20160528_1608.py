# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-28 08:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('standard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='standarditem',
            name='series',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='\u7cfb\u5217'),
        ),
        migrations.AddField(
            model_name='standarditem',
            name='vendor',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='\u5382\u5546'),
        ),
        migrations.AlterField(
            model_name='standarditem',
            name='brand',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='\u54c1\u724c'),
        ),
    ]
