# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-22 04:20
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0010_store_complete_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='storeitem',
            name='candidates',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(), null=True, size=None, verbose_name='\u53ef\u80fd\u6807\u54c1ID'),
        ),
        migrations.AddField(
            model_name='storeitem',
            name='candidates_scores',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), null=True, size=None, verbose_name='\u53ef\u80fd\u6807\u54c1ID\u5206\u6570'),
        ),
        migrations.AddField(
            model_name='storeitem',
            name='opeartor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='verified_items', to=settings.AUTH_USER_MODEL, verbose_name='\u5ba1\u6838\u54e1'),
        ),
    ]
