# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-19 12:30
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0029_auto_20160805_1442'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreShelf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shelf_id', models.PositiveIntegerField(verbose_name='\u8d27\u67b6ID')),
                ('item_ids', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(), null=True, size=None, verbose_name='\u5546\u54c1IDs')),
                ('layer', models.PositiveIntegerField(verbose_name='\u5c42')),
                ('created_at', models.DateField(verbose_name='\u751f\u6210\u65e5\u671f')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shelves', to='store.Store', verbose_name='\u5546\u5e97')),
            ],
            options={
                'verbose_name': '\u8d27\u67b6',
                'verbose_name_plural': '\u8d27\u67b6',
            },
        ),
        migrations.AlterUniqueTogether(
            name='storeshelf',
            unique_together=set([('store', 'shelf_id', 'created_at')]),
        ),
    ]