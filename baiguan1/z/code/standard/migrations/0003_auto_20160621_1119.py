# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-21 03:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('standard', '0002_auto_20160528_1608'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='standarditem',
            name='keywords',
        ),
        migrations.AlterField(
            model_name='standarditem',
            name='category',
            field=models.CharField(blank=True, choices=[('tea', '\u8336\u996e\u6599\u7c7b'), ('protein_drinks', '\u86cb\u767d\u996e\u6599\u7c7b'), ('powdered_drinks', '\u56fa\u4f53\u996e\u6599\u7c7b'), ('juice', '\u679c\u6c41\u53ca\u852c\u83dc\u6c41\u7c7b'), ('water', '\u74f6\uff08\u6876\uff09\u88c5\u996e\u7528\u6c34\u7c7b'), ('other_drinks', '\u5176\u5b83\u996e\u6599\u7c7b'), ('coffee_milktea', '\u5496\u5561/\u5976\u8336'), ('soft_drinks', '\u78b3\u9178\u996e\u6599\uff08\u6c7d\u6c34\uff09\u7c7b'), ('fast_food', '\u65b9\u4fbf\u98df\u54c1'), ('biscuit', '\u997c\u5e72\u7cd5\u70b9')], max_length=100, null=True, verbose_name='\u5206\u7c7b'),
        ),
        migrations.AlterField(
            model_name='standarditem',
            name='status',
            field=models.CharField(choices=[(b'pending_review', '\u5f85\u5ba1\u6838'), (b'human_verified', '\u5df2\u901a\u8fc7\u4eba\u5de5\u5ba1\u6838'), (b'auto_verified', '\u5df2\u901a\u8fc7\u81ea\u52a8\u5ba1\u6838')], default=b'human_verified', max_length=100, verbose_name='\u72b6\u6001'),
        ),
    ]
