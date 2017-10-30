# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-04 08:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('standard', '0020_standardvendorseriescategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='StandardSeries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[(b'pending_review', '\u5f85\u5ba1\u6838'), (b'human_verified', '\u5df2\u901a\u8fc7\u4eba\u5de5\u5ba1\u6838'), (b'na', '\u4e0d\u5904\u7406')], default=b'pending_review', max_length=100, verbose_name='\u72b6\u6001')),
                ('vendor_short_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u4f01\u4e1a\u7b80\u79f0')),
                ('brand', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u54c1\u724c')),
                ('series', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u7cfb\u5217')),
                ('last_updated', models.DateTimeField(auto_now=True, verbose_name='\u6700\u540e\u66f4\u65b0\u65f6\u95f4')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u751f\u6210\u65e5\u671f')),
            ],
            options={
                'verbose_name': '\u7cfb\u5217\u5206\u7c7b',
                'verbose_name_plural': '\u7cfb\u5217\u5206\u7c7b',
            },
        ),
        migrations.RemoveField(
            model_name='standardvendorseriescategory',
            name='category',
        ),
        migrations.RemoveField(
            model_name='standardvendorseriescategory',
            name='operator',
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': '\u5546\u54c1\u5206\u7c7b', 'verbose_name_plural': '\u5546\u54c1\u5206\u7c7b'},
        ),
        migrations.RenameField(
            model_name='standarditem',
            old_name='series',
            new_name='series_old',
        ),
        migrations.RemoveField(
            model_name='standarditem',
            name='category_old',
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, verbose_name='\u5206\u7c7b\u540d'),
        ),
        migrations.AlterField(
            model_name='standarditem',
            name='status',
            field=models.CharField(choices=[(b'pending_review', '\u5f85\u5ba1\u6838'), (b'half_verified', '\u534a\u5ba1\u6838'), (b'human_verified', '\u5df2\u901a\u8fc7\u4eba\u5de5\u5ba1\u6838'), (b'auto_verified', '\u5df2\u901a\u8fc7\u81ea\u52a8\u5ba1\u6838'), (b'na', '\u4e0d\u5904\u7406')], default=b'human_verified', max_length=100, verbose_name='\u72b6\u6001'),
        ),
        migrations.AlterField(
            model_name='standardvendor',
            name='status',
            field=models.CharField(choices=[(b'pending_review', '\u5f85\u5ba1\u6838'), (b'human_verified', '\u5df2\u901a\u8fc7\u4eba\u5de5\u5ba1\u6838'), (b'na', '\u4e0d\u5904\u7406')], default=b'pending_review', max_length=100, verbose_name='\u72b6\u6001'),
        ),
        migrations.DeleteModel(
            name='StandardVendorSeriesCategory',
        ),
        migrations.AddField(
            model_name='standardseries',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vendor_series', to='standard.Category', verbose_name='\u5bf9\u5e94\u5546\u54c1\u5206\u7c7b'),
        ),
        migrations.AddField(
            model_name='standardseries',
            name='operator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='verified_vendor_series_category', to=settings.AUTH_USER_MODEL, verbose_name='\u5ba1\u6838\u54e1'),
        ),
    ]
