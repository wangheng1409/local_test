# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-25 05:50
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('standard', '0037_auto_20161024_1352'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagsStandardSeries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None, verbose_name='\u6807\u7b7e')),
                ('status', models.CharField(choices=[(b'pending_review', '\u5f85\u5ba1\u6838'), (b'human_verified', '\u5df2\u901a\u8fc7\u4eba\u5de5\u5ba1\u6838'), (b'na', '\u4e0d\u5904\u7406')], default=b'pending_review', max_length=100, verbose_name='\u72b6\u6001')),
                ('last_updated', models.DateTimeField(auto_now=True, verbose_name='\u6700\u540e\u66f4\u65b0\u65f6\u95f4')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u751f\u6210\u65e5\u671f')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tag_series', to='standard.Category', verbose_name='\u5bf9\u5e94\u5546\u54c1\u5206\u7c7b')),
                ('operator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='verified_tag_series', to=settings.AUTH_USER_MODEL, verbose_name='\u5ba1\u6838\u54e1')),
            ],
            options={
                'verbose_name': '\u6807\u6e96\u7cfb\u5217',
                'verbose_name_plural': '\u6807\u6e96\u7cfb\u5217',
            },
        ),
        migrations.AlterUniqueTogether(
            name='tagsstandardseries',
            unique_together=set([('tags', 'category')]),
        ),
    ]
