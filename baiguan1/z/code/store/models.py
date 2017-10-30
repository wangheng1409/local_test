#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from core import choices
from standard.models import StandardItem, StandardCompany, Category
from core.models import ToDictModel
from user.models import CMUser
from django.contrib.postgres.fields import ArrayField
from os.path import join
from django.contrib.auth.models import AbstractUser
import uuid


class City(models.Model):
    name = models.CharField(verbose_name=u'名称', max_length=255)
    level = models.SmallIntegerField(verbose_name=u'层')
    parent_id = models.SmallIntegerField(verbose_name=u'父层')

    adcode = models.CharField(max_length=20, verbose_name=u'区域编号', null=True)

    # 'lat, lng; lat,lng;'
    polyline = models.TextField(verbose_name=u'区域边界', null=True, blank=True)

    def __unicode__(self):
        return u'%s' % (self.name,)

    class Meta:
        verbose_name = u'省／市／區'
        verbose_name_plural = u'省／市／區'
        unique_together = (('name', 'level', 'parent_id'))


class TradingArea(models.Model):
    city = models.ForeignKey(City, verbose_name=u'城市',
                             related_name='trading_areas')
    name = models.CharField(verbose_name=u'商圈', max_length=255)

    def __unicode__(self):
        return u'%s | %s' % (self.city, self.name)

    class Meta:
        verbose_name = u'商店商圈'
        verbose_name_plural = u'商店商圈'
        unique_together = (('city', 'name'))


class StoreTag(models.Model):
    name = models.CharField(verbose_name=u'标签', max_length=255, unique=True)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = u'商店标签'
        verbose_name_plural = u'商店标签'


class CustomerType(models.Model):
    name = models.CharField(verbose_name=u'人群', max_length=255, unique=True)

    def __unicode__(self):
        return u'%s' % (self.name)

    class Meta:
        verbose_name = u'覆盖人群'
        verbose_name_plural = u'覆盖人群'


class Entity(models.Model):
    name = models.CharField(max_length=200, verbose_name=u'名称', db_index=True)
    type = models.CharField(max_length=30, choices=choices.ENTITY_TYPE_CHOICES, verbose_name=u'类别',
                            default='convenience_store')
    city_path = models.CharField(verbose_name=u'城市 ID 路径', max_length=100, null=True, blank=True)
    lat = models.DecimalField(
        verbose_name=u'Lat', decimal_places=15, max_digits=20, blank=True, null=True)
    lng = models.DecimalField(
        verbose_name=u'Lng', decimal_places=15, max_digits=20, blank=True, null=True)
    # tag = models.CharField(max_length=200, verbose_name=u'标签', blank=True)
    address = models.CharField(max_length=512, verbose_name=u'地址', blank=True)
    telephone = models.CharField(max_length=200, verbose_name=u'电话', blank=True)
    amap_id = models.CharField(max_length=200, verbose_name=u'高德地图ID', unique=True, null=True, blank=True)
    baidu_map_id = models.CharField(max_length=200, verbose_name=u'百度地图ID', unique=True, null=True, blank=True)

    # uid = models.CharField(max_length=30, verbose_name=u'唯一标识', blank=True)

    class Meta:
        verbose_name = u'实体店'
        verbose_name_plural = u'实体店'

    def __unicode__(self):
        return self.name


class CooperativeEntity(models.Model):
    entity = models.OneToOneField(Entity, verbose_name=u'合作商店', related_name='co_entity', null=True)
    dialed = models.BooleanField(verbose_name=u'是否拨通电话', default=False)
    has_pos = models.BooleanField(verbose_name=u'是否有POS机', default=False)
    all_print = models.BooleanField(verbose_name=u'是否全部打印', default=False)
    printer_installed = models.BooleanField(verbose_name=u'是否装配打印机', default=False)
    postscript = models.TextField(verbose_name=u'备注', null=True, blank=True)
    class Meta:
        verbose_name = u'合作商家'
        verbose_name_plural = u'合作商家'

    def __unicode__(self):
        return self.entity.name

class ChainStore(models.Model):
    name = models.CharField(verbose_name = u'连锁店', max_length = 255)
    owner = models.ForeignKey(CMUser, verbose_name = u'店主')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'连锁店'
        verbose_name_plural = u'连锁店'

class StoreCategory(models.Model):
    store = models.ForeignKey(ChainStore, verbose_name=u'商店', related_name='category')
    name = models.CharField(verbose_name = u'商店分类', max_length = 100)
    parent = models.ForeignKey('self', verbose_name = u'上级分类', related_name = 'children', blank = True, null=True)
    level = models.PositiveIntegerField(verbose_name = u'层')
    created_at  = models.DateTimeField(verbose_name = u'生成日期', auto_now_add = True)
    std_category = models.ForeignKey(Category, verbose_name=u'标准分类', related_name='store_categories', blank = True, null=True)
    last_updated = models.DateTimeField(verbose_name = u'最后更新时间', auto_now = True)
    operator = models.ForeignKey(CMUser, verbose_name = u'审核員', related_name = 'verified_store_categories', null=True)
    foreign_id = models.CharField(verbose_name=u'第三方数据库原始id', max_length=100, null=True, db_index=True)

    def __unicode__(self):
        return u'%s | %s | %s' % (self.store, self.level, self.name)

    class Meta:
        verbose_name = u'商店商品分类'
        verbose_name_plural = u'商店商品分类'
        unique_together = (('store', 'name', 'level'))

class Store(models.Model, ToDictModel):
    keeper = models.ForeignKey(CMUser, verbose_name = u'店主', null=True)
    store_id = models.PositiveIntegerField(verbose_name = u'StoreID', unique=True)
    name = models.CharField(verbose_name = u'商店', max_length = 255)
    address = models.CharField(verbose_name = u'商店地址', max_length = 255, null=True)
    lat = models.DecimalField(verbose_name = u'Lat', decimal_places=15, max_digits=20, blank = True, null=True)
    lng = models.DecimalField(verbose_name = u'Lng', decimal_places=15, max_digits=20, blank = True, null=True)
    city_path = models.CharField(verbose_name = u'城市 ID 路径', max_length = 100, blank = True, null=True)
    city = models.ForeignKey(City, verbose_name=u'所在区域', blank=True, null=True)
    contact_name = models.CharField(verbose_name = u'联系人', max_length = 255, blank = True, null=True)
    contact_phone = models.CharField(verbose_name = u'联系人电话', max_length = 20, blank = True, null=True)
    bussiness_hours = models.CharField(verbose_name = u'营业时间', choices=choices.STORE_BUSSINESS_HOURS, max_length = 20, blank = True, null=True)
    store_scale = models.CharField(verbose_name = u'商店规模', choices=choices.STORE_SCALES, max_length = 100, blank = True, null=True)
    tags = ArrayField(models.PositiveIntegerField(), verbose_name = u'标签', blank = True, null=True)
    customer_types = ArrayField(models.PositiveIntegerField(), verbose_name = u'覆盖人群', blank = True, null=True)
    trading_area = models.ForeignKey(TradingArea, verbose_name = u'商店商圈', related_name = 'stores', blank = True, null=True)
    receipt_printing_freq = models.CharField(verbose_name = u'打票頻次', choices=choices.STORE_RECEIPT_PRINTING_FREQUENCE, max_length = 100, blank = True, null=True, default='all')
    chainstore = models.ForeignKey(ChainStore, verbose_name=u'连锁店', related_name='stores', blank = True, null=True)
    complete_rate = models.FloatField(verbose_name = u'完成度', default=0)
    num_sku = models.PositiveIntegerField(verbose_name = u'SKU', default=0)
    num_new_items = models.PositiveIntegerField(verbose_name = u'新品数', default=0)
    num_pending_items = models.PositiveIntegerField(verbose_name = u'待审核商品数', default=0)
    num_na = models.PositiveIntegerField(verbose_name = u'不处理商品数', default=0)
    num_verified_items = models.PositiveIntegerField(verbose_name = u'标品数', default=0)
    last_updated = models.DateTimeField(verbose_name = u'最后更新时间', auto_now = True)
    created = models.DateTimeField(verbose_name = u'创建时间', null=True)

    def __unicode__(self):
        # return u'%s | %s' % (self.name, self.address)
        return self.name

    class Meta:
        verbose_name = u'商店'
        verbose_name_plural = u'商店'


class StoreDailyTarget(models.Model):
    date = models.DateField(verbose_name=u'日期')
    sales = models.FloatField(verbose_name=u'销售额')
    store = models.ForeignKey(Store, verbose_name=u'商店',
                              related_name='sale_targets',
                              blank=True,
                              null=True)

    class Meta:
        verbose_name = u'日销售任务'
        verbose_name_plural = u'日销售任务'
        unique_together = (('date', 'store'))


class Attribute(models.Model):
    attr_type = models.CharField(verbose_name=u'属性类别', max_length=100,
                                 db_index=True)
    foreign_id = models.CharField(verbose_name=u'对方数据库id',
                                  max_length=100,
                                  null=True,
                                  db_index=True)
    name = models.CharField(verbose_name=u'属性名称', max_length=100)
    chainstore = models.ForeignKey(ChainStore, verbose_name=u'连锁店',
                                   related_name='attributes',
                                   null=True)

    class Meta:
        verbose_name = u'商店属性'
        verbose_name_plural = u'商店属性'
        unique_together = (("attr_type", "name", "chainstore"),)


class AttributeMap(models.Model):
    store = models.ForeignKey(Store,
                              verbose_name=u'商店',
                              related_name='attributes')
    attribute = models.ForeignKey(Attribute,
                                  verbose_name=u'属性',
                                  related_name='stores')

    class Meta:
        unique_together = (('store', 'attribute'))


class StoreCompanyStats(models.Model):
    store = models.ForeignKey(Store, verbose_name=u'商店', related_name='stats')
    company = models.ForeignKey(
        StandardCompany, verbose_name=u'品牌', related_name='store_stats')

    complete_rate = models.FloatField(verbose_name=u'完成度', default=0)
    num_sku = models.PositiveIntegerField(verbose_name=u'SKU', default=0)
    num_new = models.PositiveIntegerField(verbose_name=u'新品数', default=0)
    num_pending_items = models.PositiveIntegerField(
        verbose_name=u'待审核商品数', default=0)
    num_na = models.PositiveIntegerField(verbose_name=u'不处理商品数', default=0)
    num_verified_items = models.PositiveIntegerField(
        verbose_name=u'标品数', default=0)
    last_updated = models.DateTimeField(verbose_name=u'最后更新时间', auto_now=True)
    created_at = models.DateTimeField(verbose_name=u'生成日期', auto_now_add=True)

    def __unicode__(self):
        return u'%s | %s | %.2f' % (self.store, self.company, self.complete_rate)

    class Meta:
        verbose_name = u'商店品牌進度'
        verbose_name_plural = u'商店品牌進度'
        unique_together = (('store', 'company'))

def store_item_upload(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return join('store_item',  filename)


class StoreItemState(models.Model):
    foreign_id = models.CharField(verbose_name=u'第三方ID', max_length=100,
                                  db_index=True, null=True)
    chainstore = models.ForeignKey(ChainStore,
                                   verbose_name=u'定义该状态的连锁店', null=True)
    name = models.CharField(verbose_name=u'名称', max_length=100, unique=True,
                            db_index=True)



class StoreItem(models.Model, ToDictModel):
    store = models.ForeignKey(
        Store, verbose_name=u'商店', related_name='items', blank=True, null=True)
    company = models.ForeignKey(
        StandardCompany, verbose_name=u'品牌', related_name='store_items', blank=True, null=True)
    standard_item = models.ForeignKey(
        StandardItem, verbose_name=u'标准化商品', related_name='store_items', blank=True, null=True)
    receipt_item_id = models.CharField(
        verbose_name=u'小票商品ID', max_length=255, db_index=True, blank=True, null=True)

    name = models.CharField(verbose_name=u'商品名', max_length=255, db_index=True)
    price = models.FloatField(verbose_name=u'售价')
    status = models.CharField(verbose_name=u'状态', max_length=255,
                              choices=choices.STORE_ITEM_STATUS, default='under_review')
    # disambiguation_detail = models.TextField(verbose_name = u'匹配详情', blank = True, null=True)
    trade_at = models.DateTimeField(verbose_name=u'生成日期')
    last_updated = models.DateTimeField(verbose_name=u'最后更新时间', auto_now=True)

    keywords = ArrayField(models.TextField(), verbose_name=u'关键词', null=True)
    vector = ArrayField(models.PositiveIntegerField(),
                        verbose_name=u'Vector', null=True)

    candidates = ArrayField(models.PositiveIntegerField(), verbose_name = u'可能标品ID', null=True)
    candidates_scores = ArrayField(models.FloatField(), verbose_name = u'可能标品ID分数', null=True)
    operator = models.ForeignKey(CMUser, verbose_name = u'审核員', related_name = 'verified_items', null=True)
    image_url = models.TextField(verbose_name = u'商品图URL', blank = True, null=True)
    image = models.ImageField(verbose_name = u'商品图',
                              upload_to = store_item_upload,
                              blank = True, null=True)
    store_cat = models.ForeignKey(StoreCategory,
                                  verbose_name=u'商品类别',
                                  related_name='store_items',
                                  null=True)
    chain_store = models.ForeignKey(ChainStore,
                                    verbose_name=u'连锁店',
                                    related_name='chain_store_items',
                                    null=True)
    item_state = models.ForeignKey(StoreItemState,
                                   verbose_name=u'商品状态',
                                   null=True)

    def __unicode__(self):
        return u'%s | %s' % (self.name, self.store)

    class Meta:
        verbose_name = u'商品'
        verbose_name_plural = u'商品'
        unique_together = (('store', 'chain_store', 'name'), ('store', 'name'), ('chain_store', 'name', 'receipt_item_id'))


class StoreItemInventory(models.Model):
    store = models.ForeignKey(Store, verbose_name=u'商店',
                              related_name='inventory')
    store_item = models.ForeignKey(StoreItem,
                                   verbose_name=u'商店商品',
                                   blank=True, null=True,
                                   related_name='inventory')
    purchase_price = models.FloatField(verbose_name=u'进货价格')
    quantity = models.FloatField(verbose_name=u'库存')
    tax = models.FloatField(verbose_name=u'税额 ', null=True)
    fill_date  = models.DateField(verbose_name=u'生成日期')

    class Meta:
        verbose_name = "StoreItemInventory"
        verbose_name_plural = "StoreItemInventories"
        unique_together = (('fill_date', 'store', 'store_item'))

    def __unicode__(self):
        pass


class ChainStoreItemInventory(models.Model):
    chain_store = models.OneToOneField(ChainStore,
                                       verbose_name=u'连锁店')
    store_item = models.ForeignKey(StoreItem, verbose_name=u'商店商品')
    purchase_price = models.FloatField(verbose_name=u'进货价格')
    quantity = models.FloatField(verbose_name=u'库存')
    tax = models.FloatField(verbose_name=u'税额 ', null=True)
    fill_date  = models.DateField(verbose_name=u'生成日期')

    class Meta:
        verbose_name = u'连锁店大仓库存'
        verbose_name_plural = u'连锁店大仓库存'
        unique_together = (('fill_date', 'store_item', 'chain_store'))


def store_shelf_upload(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return join('store_shelf',  filename)

class StoreShelf(models.Model, ToDictModel):
    store = models.ForeignKey(Store, verbose_name = u'商店', related_name = 'shelves')
    shelf_id = models.PositiveIntegerField(verbose_name = u'货架ID')
    item_ids = ArrayField(models.PositiveIntegerField(), verbose_name = u'商品IDs', null=True)
    layer = models.PositiveIntegerField(verbose_name = u'层')
    image = models.ImageField(verbose_name = u'货架图', upload_to = store_shelf_upload, blank = True, null=True)
    created_at  = models.DateField(verbose_name = u'生成日期')

    def __unicode__(self):
        if self.id:
            return u'%s | %s' % (self.store, self.id)

    class Meta:
        verbose_name = u'货架'
        verbose_name_plural = u'货架'
        unique_together = (('store', 'shelf_id', 'created_at'))


class ScoredOnlineItem(object):
    @classmethod
    def get_scored_online_items():
        pass

class TransactionAccount(models.Model):
    user = models.OneToOneField(CMUser, verbose_name=u'用户')
    wechat_mch_id = models.CharField(max_length=200, verbose_name=u'微信支付商户号', null=True, blank=True)
    wechat_appid = models.CharField(max_length=200, verbose_name=u'微信公众账号APPID', null=True, blank=True)
    wechat_username = models.CharField(max_length=200, verbose_name=u'微信商户平台登录账号', null=True, blank=True)
    wechat_password = models.CharField(max_length=200, verbose_name=u'微信商户平台登录密码', null=True, blank=True)
    wechat_api_key = models.CharField(max_length=200, verbose_name=u'微信商户平台Api密钥', null=True, blank=True)

    alipay_username = models.CharField(max_length=200, verbose_name=u'支付宝用户名', null=True, blank=True)
    alipay_password = models.CharField(max_length=200, verbose_name=u'支付宝登录密码', null=True, blank=True)
    alipay_pid = models.CharField(max_length=200, verbose_name=u'支付宝合作者身份(PID)', null=True, blank=True)
    alipay_key = models.CharField(max_length=200, verbose_name=u'支付宝安全校验码(KEY)', null=True, blank=True)
    alipay_appid = models.CharField(max_length=200, verbose_name=u'支付宝APPID', null=True, blank=True)
    class Meta:
        verbose_name = "商店交易账户信息"
        verbose_name_plural = "商店交易账户信息"

    def __str__(self):
        pass


class ThirdPartyDBInfo(models.Model, ToDictModel):
    user = models.ForeignKey(CMUser,
                             verbose_name=u'创建人',
                             related_name='con_db_info')
    dbtype = models.SmallIntegerField(verbose_name=u'数据库类型')
    dbhost = models.CharField(verbose_name=u'数据库地址',
                              max_length=255)
    dbuser = models.CharField(verbose_name=u'数据库用户名',
                              max_length=50)
    dbname = models.CharField(verbose_name=u'数据库名',
                              max_length=50, null=True)
    dbpassword = models.CharField(verbose_name=u'数据库密码',
                                  max_length=255)
    dbport = models.CharField(verbose_name=u'数据库端口',
                              max_length=50,
                              null=True)



class ThirdPartyDBTables(models.Model):
    db = models.ForeignKey(ThirdPartyDBInfo,
                           verbose_name=u'数据库',
                           related_name=u'tables')
    name = models.CharField(verbose_name=u'表名',
                            max_length=255)
    trigger_name = models.CharField(max_length=255, null=True)
    do_fetch = models.BooleanField(u'是否读取该表数据', default=False)
    fetch_interval = models.IntegerField(verbose_name=u'读取间隔', null=True)

class DistrictInfo(models.Model):
    district = models.OneToOneField(City, verbose_name=u'区域', null=True)
    gdp = models.BigIntegerField(verbose_name=u'总GDP(元)', null=True)
    residents = models.IntegerField(verbose_name=u'常住人口(人)', null=True)
    area = models.IntegerField(verbose_name=u'区域面积(km²)', null=True)
    population_density = models.IntegerField(verbose_name=u'人口密度(人/km²)', null=True)
    pgdp = models.IntegerField(verbose_name=u'人均GDP(元)', null=True)

    class Meta:
        verbose_name = "区域详情"
        verbose_name_plural = "区域详情"

    def __unicode__(self):
        return self.district.name


class UAC(models.Model):
    store_area_permission = models.ManyToManyField(Attribute, verbose_name=u'区域权限')
    store_category_permission = models.ManyToManyField(StoreCategory, verbose_name=u'品类权限')
    chain_store_permission = models.ForeignKey(ChainStore, verbose_name=u'便利店权限', null=True)
    login_to_url = models.CharField(max_length=200, null=True)


class StoreUser(models.Model):
    user = models.OneToOneField(CMUser, verbose_name=u'负责人')
    permission = models.ForeignKey(UAC, verbose_name=u'操作权限', null=True)
