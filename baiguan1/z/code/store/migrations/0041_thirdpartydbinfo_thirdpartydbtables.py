# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-17 08:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0040_store_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThirdPartyDBInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dbtype', models.SmallIntegerField(verbose_name='\u6570\u636e\u5e93\u7c7b\u578b')),
                ('dbhost', models.CharField(max_length=255, verbose_name='\u6570\u636e\u5e93\u5730\u5740')),
                ('dbuser', models.CharField(max_length=50, verbose_name='\u6570\u636e\u5e93\u7528\u6237\u540d')),
                ('dbname', models.CharField(max_length=50, verbose_name='\u6570\u636e\u5e93\u540d')),
                ('dbpassword', models.CharField(max_length=255, verbose_name='\u6570\u636e\u5e93\u5bc6\u7801')),
                ('dbport', models.CharField(max_length=50, null=True, verbose_name='\u6570\u636e\u5e93\u7aef\u53e3')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='con_db_info', to=settings.AUTH_USER_MODEL, verbose_name='\u521b\u5efa\u4eba')),
            ],
        ),
        migrations.CreateModel(
            name='ThirdPartyDBTables',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='\u8868\u540d')),
                ('trigger_name', models.CharField(max_length=255)),
                ('do_fetch', models.BooleanField(default=False, verbose_name='\u662f\u5426\u8bfb\u53d6\u8be5\u8868\u6570\u636e')),
                ('fetch_interval', models.IntegerField(null=True, verbose_name='\u8bfb\u53d6\u95f4\u9694')),
                ('db', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tables', to='store.ThirdPartyDBInfo', verbose_name='\u6570\u636e\u5e93')),
            ],
        ),
    ]
