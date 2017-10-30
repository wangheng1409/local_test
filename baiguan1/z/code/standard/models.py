#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from core import choices
from core.models import ToDictModel
from django.contrib.postgres.fields import ArrayField
from user.models import CMUser
from xpinyin import Pinyin

class Category(models.Model):
    name = models.CharField(verbose_name = u'分类名', max_length = 100)
    parent = models.ForeignKey('self', verbose_name = u'上级分类', related_name = 'children', blank = True, null=True)
    level = models.PositiveIntegerField(verbose_name = u'层')
    created_at  = models.DateTimeField(verbose_name = u'生成日期', auto_now_add = True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'商品分类'
        verbose_name_plural = u'商品分类'

class StandardCompany(models.Model):
    name = models.CharField(verbose_name = u'企业简称', max_length = 255, blank = True, null=True, unique=True)
    num_vendors = models.PositiveIntegerField(verbose_name = u'生產厂商数', default=0)
    num_sku = models.PositiveIntegerField(verbose_name = u'SKU', default=0)
    num_pending_items = models.PositiveIntegerField(verbose_name = u'待审核商品数', default=0)
    num_verified_items = models.PositiveIntegerField(verbose_name = u'标品数', default=0)
    num_na = models.PositiveIntegerField(verbose_name = u'不处理数', default=0)
    num_new = models.PositiveIntegerField(verbose_name = u'新品数', default=0)
    complete_rate = models.FloatField(verbose_name = u'完成度', default=0)

    keywords = ArrayField(models.TextField(), verbose_name = u'关键词', null=True)
    vector = ArrayField(models.PositiveIntegerField(), verbose_name = u'Vector', null=True)

    created_at  = models.DateTimeField(verbose_name = u'生成日期', auto_now_add = True)
    last_updated = models.DateTimeField(verbose_name = u'最后更新时间', auto_now = True)
    def __unicode__(self):
        return u'%s | %.2f%%' % (self.name, self.complete_rate)

    class Meta:
        verbose_name = u'企业'
        verbose_name_plural = u'企业'

class TagsStandardSeries(models.Model):
    tags = ArrayField(models.TextField(), verbose_name = u'标签')
    category = models.ForeignKey(Category, verbose_name = u'对应商品分类', related_name = 'tag_series')
    status = models.CharField(verbose_name = u'状态', max_length = 100, choices=choices.STANDARD_VENDOR_SERIES_CATEGORY, default='pending_review')
    last_updated = models.DateTimeField(verbose_name = u'最后更新时间', auto_now = True)
    created_at  = models.DateTimeField(verbose_name = u'生成日期', auto_now_add = True)
    operator = models.ForeignKey(CMUser, verbose_name = u'审核員', related_name = 'verified_tag_series', null=True)

    def __unicode__(self):
        return u'%s -> %s' % (self.series, self.category)

    class Meta:
        verbose_name = u'标準系列'
        verbose_name_plural = u'标準系列'
        unique_together = (('tags', 'category'), )

# @WARNING: pending deprecation, use tags_standard_series instead
class StandardSeries(models.Model):
    status = models.CharField(verbose_name = u'状态', max_length = 100, choices=choices.STANDARD_VENDOR_SERIES_CATEGORY, default='pending_review')
    vendor_short_name = models.CharField(verbose_name = u'企业简称', max_length = 255, blank = True, null=True)
    brand = models.CharField(verbose_name = u'品牌', max_length = 255, blank = True, null=True)
    series = models.CharField(verbose_name = u'系列', max_length = 255, blank = True, null=True)
    category = models.ForeignKey(Category, verbose_name = u'对应商品分类', related_name = 'vendor_series', null=True)
    last_updated = models.DateTimeField(verbose_name = u'最后更新时间', auto_now = True)
    created_at  = models.DateTimeField(verbose_name = u'生成日期', auto_now_add = True)
    operator = models.ForeignKey(CMUser, verbose_name = u'审核員', related_name = 'verified_vendor_series_category', null=True)

    def __unicode__(self):
        # return u'%s | %s | %s -> %s' % (self.vendor_short_name, self.brand, self.series, self.category)
        return u'%s -> %s' % (self.series, self.category)

    class Meta:
        verbose_name = u'系列分类'
        verbose_name_plural = u'系列分类'
        unique_together = (('vendor_short_name', 'brand', 'series'), )


class StandardVendor(models.Model):
    status = models.CharField(verbose_name = u'状态', max_length = 100, choices=choices.STANDARD_VENDOR_STATUS, default='pending_review')
    barcode = models.CharField(verbose_name = u'国际条码', max_length = 20, unique=True)
    name = models.CharField(verbose_name = u'生產厂商', max_length = 255, blank = True, null=True)
    standard_name = models.CharField(verbose_name = u'企业简称', max_length = 255, blank = True, null=True)
    num_sku = models.PositiveIntegerField(verbose_name = u'SKU', default=0)
    last_updated = models.DateTimeField(verbose_name = u'最后更新时间', auto_now = True)
    created_at  = models.DateTimeField(verbose_name = u'生成日期', auto_now_add = True)
    operator = models.ForeignKey(CMUser, verbose_name = u'审核員', related_name = 'verified_standard_vendors', null=True)

    def __unicode__(self):
        return u'%s | %s' % (self.barcode, self.name)

    class Meta:
        verbose_name = u'品牌码'
        verbose_name_plural = u'品牌码'

class StandardItem(models.Model, ToDictModel):
    status = models.CharField(verbose_name = u'状态', max_length = 100, choices=choices.STANDARD_ITEM_STATUS, default='human_verified')
    barcode = models.CharField(verbose_name = u'国际条码', max_length = 20, unique=True)
    name = models.CharField(verbose_name = u'商品名', max_length = 255, db_index=True)
    model = models.CharField(verbose_name = u'规格', max_length = 100, blank = True, null=True)
    flavor = models.CharField(verbose_name = u'口味', max_length = 100, blank = True, null=True)
    keywords = ArrayField(models.TextField(), verbose_name = u'关键词', null=True)
    num_matches = models.PositiveIntegerField(verbose_name = u'匹配商品数', default=0)

    series = models.ForeignKey(StandardSeries, verbose_name = u'系列', related_name = 'items', blank = True, null=True)
    category = models.ForeignKey(Category, verbose_name = u'分类', related_name = 'items', blank = True, null=True)

    vendor_short_name_txt = models.CharField(verbose_name = u'企业简称', max_length = 255, blank = True, null=True)
    vendor_txt = models.CharField(verbose_name = u'生產厂商', max_length = 255, blank = True, null=True)
    brand_txt = models.CharField(verbose_name = u'品牌', max_length = 255, blank = True, null=True)
    category_txt = models.CharField(verbose_name = u'分类', max_length = 255, blank = True, null=True)
    series_txt = models.CharField(verbose_name = u'系列', max_length = 255, blank = True, null=True)

    alias = ArrayField(models.TextField(), verbose_name = u'别名', null=True)
    store_prices = ArrayField(ArrayField(models.TextField()), verbose_name = u'便利店售价', null=True)
    mean = models.FloatField(verbose_name = u'平均售价', null=True)
    std_dev = models.FloatField(verbose_name = u'Std Dev', null=True)

    last_updated = models.DateTimeField(verbose_name = u'最后更新时间', auto_now = True)
    created_at  = models.DateTimeField(verbose_name = u'生成日期', auto_now_add = True)

    operator = models.ForeignKey(CMUser, verbose_name = u'审核員', related_name = 'verified_standard_items', null=True)
    source = models.CharField(verbose_name = u'來源', max_length = 100, choices=choices.STANDARD_ITEM_SOURCE, default='barcode_store')

    def __unicode__(self):
        return u'%s | %s' % (self.barcode, self.name)

    class Meta:
        verbose_name = u'标准商品'
        verbose_name_plural = u'标准商品'

class StandardTag(models.Model):
    tag = models.CharField(verbose_name = u'标签', max_length = 100, unique=True)
    type = models.CharField(verbose_name = u'类别', max_length = 100, choices=choices.STANDARD_TAG_TYPE)
    pinyin = models.CharField(verbose_name = u'拼音', max_length = 255, blank = True, null=True)
    alias = ArrayField(models.TextField(), verbose_name = u'别名', null=True)
    created_at  = models.DateField(verbose_name = u'生成日期', auto_now_add = True)

    def __unicode__(self):
        return u'[%s] %s' % (self.type, self.tag)

    def save(self, *args, **kwargs):
        if getattr(self, 'tag_changed', True):
            pinyin_client = Pinyin()
            self.tag = self.tag.upper()
            self.pinyin = pinyin_client.get_pinyin(self.tag)
        super(StandardTag, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u'标准标签'
        verbose_name_plural = u'标准标签'

