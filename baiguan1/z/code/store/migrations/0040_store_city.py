# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-12 08:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0039_auto_20161012_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.City', verbose_name='\u6240\u5728\u533a\u57df'),
        ),
    ]
