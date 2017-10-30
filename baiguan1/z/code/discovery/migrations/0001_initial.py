# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-11-02 05:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CollectionProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.BigIntegerField(verbose_name='\u5546\u54c1ID')),
                ('collect_time', models.DateTimeField(auto_now_add=True, verbose_name='\u6536\u85cf\u65f6\u95f4')),
                ('product_name', models.CharField(max_length=255, null=True, verbose_name='\u540d\u79f0')),
                ('product_image', models.TextField(blank=True, null=True, verbose_name='\u5546\u54c1\u56fe\u7247')),
                ('product_source', models.CharField(max_length=255, null=True, verbose_name='\u5546\u57ce')),
                ('product_area', models.CharField(max_length=255, null=True, verbose_name='\u5730\u533a')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='collectionproduct',
            unique_together=set([('product_id', 'product_source')]),
        ),
    ]