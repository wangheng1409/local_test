# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-13 08:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0003_customitem_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitorbarcodes',
            name='name',
            field=models.CharField(default='', max_length=255, verbose_name='\u9879\u76ee\u540d'),
            preserve_default=False,
        ),
    ]