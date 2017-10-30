#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from core import choices

class StoreItemSyncLog(models.Model):
    last_id = models.PositiveIntegerField(verbose_name = u'最後更新ID', unique=True)
    count = models.PositiveIntegerField(verbose_name = u'量')
    created_at  = models.DateTimeField(verbose_name = u'生成日期', auto_now_add = True)

    def __unicode__(self):
        return u'%s | %s | %s' % (self.last_id, self.count, self.created_at)

    class Meta:
        verbose_name = u'商店商品同步记录'
        verbose_name_plural = u'商店商品同步记录'

class BarcodeStoreItemSyncLog(models.Model):
    last_id = models.PositiveIntegerField(verbose_name = u'最後更新ID', unique=True)
    count = models.PositiveIntegerField(verbose_name = u'量')
    created_at  = models.DateTimeField(verbose_name = u'生成日期', auto_now_add = True)

    def __unicode__(self):
        return u'%s | %s | %s' % (self.last_id, self.count, self.created_at)

    class Meta:
        verbose_name = u'條碼商店商品同步记录'
        verbose_name_plural = u'條碼商店商品同步记录'

class WebFoodSafetyBarcodeSyncLog(models.Model):
    last_date = models.DateField(verbose_name = u'最後更新日期', unique=True)
    count = models.PositiveIntegerField(verbose_name = u'量')
    created_at  = models.DateTimeField(verbose_name = u'生成日期', auto_now_add = True)

    def __unicode__(self):
        return u'%s | %s | %s' % (self.last_date, self.count, self.created_at)

    class Meta:
        verbose_name = u'食品安全網站條碼同步记录'
        verbose_name_plural = u'食品安全網站條碼同步记录'

class SpiderSyncLog(models.Model):
    source = models.CharField(max_length = 255, verbose_name = '来源')
    area = models.CharField(max_length = 255, verbose_name = '地区')
    crawl_date = models.DateField(verbose_name = '爬取日期')
    tag = models.CharField(max_length = 255, verbose_name = '标签')
    count = models.IntegerField(verbose_name = '数量') 

    def __unicode__(self):
        return u'%s | %s | %s | %s | %s' % (self.source, self.area, self.crawl_date, self.tag, self.count)

    class Meta:
        verbose_name = u'爬虫同步记录'
        verbose_name_plural = u'爬虫同步记录'
