
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from user.models import CMUser

# Create your models here.

class CollectionProduct(models.Model):
    user = models.ForeignKey(CMUser, verbose_name=u'用户', null=True)
    product_id = models.BigIntegerField(verbose_name=u'商品ID')
    collect_time = models.DateTimeField(verbose_name=u'收藏时间', auto_now_add=True)
    product_name = models.CharField(verbose_name=u'名称', max_length=255, null=True)
    product_image = models.TextField(verbose_name=u'商品图片', blank = True, null=True)
    product_source = models.CharField(verbose_name=u'商城', max_length=255, null=True)
    product_area = models.CharField(verbose_name=u'地区', max_length=255, null=True)

    class Meta:
        unique_together = (('product_id', 'product_source'))