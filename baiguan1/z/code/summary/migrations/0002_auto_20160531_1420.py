# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-31 06:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('summary', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailystoreitemsummary',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='summary', to='store.StoreItem', verbose_name='\u5546\u54c1'),
        ),
    ]