# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-05 06:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0028_store_store_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='store_id',
            field=models.PositiveIntegerField(unique=True, verbose_name='StoreID'),
        ),
    ]