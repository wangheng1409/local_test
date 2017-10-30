# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-05 03:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('standard', '0022_standarditem_series'),
    ]

    operations = [
        migrations.RenameField(
            model_name='standarditem',
            old_name='brand',
            new_name='brand_txt',
        ),
        migrations.RenameField(
            model_name='standarditem',
            old_name='series_old',
            new_name='series_txt',
        ),
        migrations.RenameField(
            model_name='standarditem',
            old_name='vendor_short_name',
            new_name='vendor_short_name_txt',
        ),
        migrations.RenameField(
            model_name='standarditem',
            old_name='vendor',
            new_name='vendor_txt',
        ),
        migrations.AddField(
            model_name='standarditem',
            name='category_txt',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='\u5206\u7c7b'),
        ),
    ]