# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-21 13:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_auto_20160621_1918'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FullAccessStoreItem',
        ),
        migrations.CreateModel(
            name='FilteredStoreItem',
            fields=[
            ],
            options={
                'verbose_name': '\u5355\u5e97\u5546\u54c1',
                'proxy': True,
                'verbose_name_plural': '\u5355\u5e97\u5546\u54c1',
            },
            bases=('store.storeitem',),
        ),
    ]
