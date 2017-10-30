# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-25 13:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summary', '0010_auto_20160616_1846'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dailystoreitemsummary',
            name='category',
        ),
        migrations.RemoveField(
            model_name='monthlystoreitemsummary',
            name='category',
        ),
        migrations.AlterField(
            model_name='dailystoresummary',
            name='num_sku',
            field=models.BigIntegerField(verbose_name='\u552f\u4e00\u5546\u54c1\u6570'),
        ),
        migrations.AlterField(
            model_name='monthlystoresummary',
            name='num_sku',
            field=models.BigIntegerField(verbose_name='\u552f\u4e00\u5546\u54c1\u6570'),
        ),
        migrations.AlterUniqueTogether(
            name='dailystorecategorysummary',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='monthlystorecategorysummary',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='dailystorecategorysummary',
            name='category',
        ),
        migrations.RemoveField(
            model_name='monthlystorecategorysummary',
            name='category',
        ),
    ]