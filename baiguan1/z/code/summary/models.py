# -*- coding: utf-8 -*-

from django.db import models
from core import choices
from store.models import Store, StoreItem
from django.contrib.postgres.fields import ArrayField


class DailyStoreItemSummary(models.Model):
    date = models.DateField(verbose_name = u'日期')
    last_updated = models.DateTimeField(verbose_name = u'最后更新时间', auto_now = True)
    store = models.ForeignKey(Store, verbose_name = u'商店', related_name = 'item_summary', blank = True, null=True)
    item = models.ForeignKey(StoreItem, verbose_name = u'商品', related_name = 'summary')
    sales = models.FloatField(verbose_name = u'销售额')
    num = models.FloatField(verbose_name = u'销量')

    # for faster query
    unit_price = models.FloatField(verbose_name = u'售价', blank = True, null=True)
    model = models.CharField(verbose_name = u'规格', max_length = 100, blank = True, null=True)
    flavor = models.CharField(verbose_name = u'口味', max_length = 100, blank = True, null=True)
    category = models.CharField(verbose_name = u'口味', max_length = 100, blank = True, null=True)
    barcode = models.CharField(verbose_name = u'国际条码', max_length = 20, blank = True, null=True)

    def __unicode__(self):
        return u'%s | %s | %s' % (self.date, self.item, self.sales)

    class Meta:
        unique_together = (('date', 'store', 'item'),)
        verbose_name = u'便利店每天单品汇总'
        verbose_name_plural = u'便利店每天单品汇总'

class MonthlyStoreItemSummary(models.Model):
    date = models.IntegerField(verbose_name = u'日期(yyyymm)')
    last_updated = models.DateTimeField(verbose_name = u'最后更新时间', auto_now = True)
    store = models.ForeignKey(Store, verbose_name = u'商店', related_name = 'monthly_item_summary', blank = True, null=True)
    item = models.ForeignKey(StoreItem, verbose_name = u'商品', related_name = 'monthly_summary')
    sales = models.FloatField(verbose_name = u'销售额')
    num = models.FloatField(verbose_name = u'销量')

    # for faster query
    unit_price = models.FloatField(verbose_name = u'售价', blank = True, null=True)
    model = models.CharField(verbose_name = u'规格', max_length = 100, blank = True, null=True)
    flavor = models.CharField(verbose_name = u'口味', max_length = 100, blank = True, null=True)
    category = models.CharField(verbose_name = u'口味', max_length = 100, blank = True, null=True)
    barcode = models.CharField(verbose_name = u'国际条码', max_length = 20, blank = True, null=True)

    def __unicode__(self):
        return u'%s | %s | %s' % (self.date, self.item, self.sales)

    class Meta:
        unique_together = (('date', 'store', 'item'),)
        verbose_name = u'便利店每月单品汇总'
        verbose_name_plural = u'便利店每月单品汇总'

"""
    Use cases:
    * For store's owner, daily stats
    * For us, 1. we can compare store, 2. find similar store
"""
class DailyStoreSummary(models.Model):
    date = models.DateField(verbose_name = u'日期')
    last_updated = models.DateTimeField(verbose_name = u'最后更新时间', auto_now = True)
    store = models.ForeignKey(Store, verbose_name = u'商店', related_name = 'summary', blank = True, null=True)
    num_sku = models.BigIntegerField(verbose_name = u'唯一商品数')
    sales = models.FloatField(verbose_name = u'销售额')
    num = models.FloatField(verbose_name = u'销量')
    num_trades = models.FloatField(verbose_name = u'交易数', null=True)

    def __unicode__(self):
        return u'%s | %s | %s' % (self.date, self.store, self.sales)

    class Meta:
        unique_together = (('date', 'store'),)

class MonthlyStoreSummary(models.Model):
    date = models.IntegerField(verbose_name = u'日期(yyyymm)')
    last_updated = models.DateTimeField(verbose_name = u'最后更新时间', auto_now = True)
    store = models.ForeignKey(Store, verbose_name = u'商店', related_name = 'monthly_summary', blank = True, null=True)
    num_sku = models.BigIntegerField(verbose_name = u'唯一商品数')
    sales = models.FloatField(verbose_name = u'销售额')
    num = models.FloatField(verbose_name = u'销量')
    num_trades = models.FloatField(verbose_name = u'交易数', null=True)

    def __unicode__(self):
        return u'%s | %s | %s' % (self.date, self.store, self.sales)


    class Meta:
        unique_together = (('date', 'store'),)

"""
    Use cases:
    * add-on infor for daily store summary
"""
class DailyStoreCategorySummary(models.Model):
    date = models.DateField(verbose_name = u'日期')
    last_updated = models.DateTimeField(verbose_name = u'最后更新时间', auto_now = True)
    store = models.ForeignKey(Store, verbose_name = u'商店', related_name = 'category_summary', blank = True, null=True)
    category_id = models.PositiveIntegerField(verbose_name = u'分类ID', null=True)
    sales = models.FloatField(verbose_name = u'销售额')
    num = models.FloatField(verbose_name = u'销量')

    def __unicode__(self):
        return u'%s | %s | %s | %s' % (self.date, self.category_id, self.store, self.sales)

    class Meta:
        unique_together = (('date', 'store', 'category_id'),)

class MonthlyStoreCategorySummary(models.Model):
    date = models.IntegerField(verbose_name = u'日期(yyyymm)')
    last_updated = models.DateTimeField(verbose_name = u'最后更新时间', auto_now = True)
    store = models.ForeignKey(Store, verbose_name = u'商店', related_name = 'monthly_category_summary', blank = True, null=True)
    category_id = models.PositiveIntegerField(verbose_name = u'分类ID', null=True)
    sales = models.FloatField(verbose_name = u'销售额')
    num = models.FloatField(verbose_name = u'销量')

    def __unicode__(self):
        return u'%s | %s | %s | %s' % (self.date, self.category_id, self.store, self.sales)

    class Meta:
        unique_together = (('date', 'store', 'category_id'),)

"""
    Use cases:
    input: store_id, an item
    output: items are bought together, frequency
"""
class MonthlyStoreItemPattern(models.Model):
    date = models.IntegerField(verbose_name = u'日期')
    last_updated = models.DateTimeField(verbose_name = u'最后更新时间', auto_now = True)
    store = models.ForeignKey(Store, verbose_name = u'商店', related_name = 'monthly_patterns')
    patterns = ArrayField(models.TextField(), verbose_name = u'商品名', null=True, blank = True)
    frequency = models.PositiveIntegerField(verbose_name = u'频次')

    def __unicode__(self):
        return u'%s | %s | %s | %s' % (self.date, self.store, self.patterns, self.frequency)

    class Meta:
        unique_together = (('date', 'store', 'patterns'),)
        verbose_name = u'同时购买商品'
        verbose_name_plural = u'同时购买商品'






