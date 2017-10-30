# -*- coding: utf-8 -*-

from django.db import models
from core import choices
from django.contrib.postgres.fields import ArrayField
from user.models import CMUser

class CustomItem(models.Model):
    barcode = models.CharField(verbose_name = u'国际条码', max_length = 20, unique=True)
    name = models.CharField(verbose_name = u'商品名', max_length = 255, db_index=True)
    model = models.CharField(verbose_name = u'规格', max_length = 100, blank = True, null=True)
    flavor = models.CharField(verbose_name = u'口味', max_length = 100, blank = True, null=True)
    series = models.CharField(verbose_name = u'系列', max_length = 100, blank = True, null=True)
    category = models.CharField(verbose_name = u'分类', max_length = 100, blank = True, null=True)

    last_updated = models.DateTimeField(verbose_name = u'最后更新时间', auto_now = True)
    created_at  = models.DateTimeField(verbose_name = u'生成日期', auto_now_add = True)

    owner = models.ForeignKey(CMUser, verbose_name = u'用戶', related_name = 'custom_items')

    def __unicode__(self):
        return u'%s | %s' % (self.barcode, self.name)

    class Meta:
        verbose_name = u'品牌自定议商品'
        verbose_name_plural = u'品牌自定议商品'

class MonitorBarcodes(models.Model):
    name = models.CharField(verbose_name = u'项目名', max_length = 255)
    user = models.ForeignKey(CMUser, verbose_name = u'用戶', related_name = 'monitor_barcodes', null=True)
    barcodes = models.ManyToManyField(CustomItem, verbose_name = u'定议商品', related_name = 'monitors')

    start_date = models.DateField(verbose_name = u'开始日期', blank = True, null=True)
    end_date = models.DateField(verbose_name = u'結束日期', blank = True, null=True)

    last_updated = models.DateTimeField(verbose_name = u'最后更新时间', auto_now = True)
    created_at  = models.DateTimeField(verbose_name = u'生成日期', auto_now_add = True)

    def __unicode__(self):
        return u'%s' % (self.user, )

    class Meta:
        verbose_name = u'品牌商品监测管理'
        verbose_name_plural = u'品牌商品监测管理'