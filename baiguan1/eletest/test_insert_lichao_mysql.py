# !/usr/bin/env python
# -*- coding:utf-8 -*-
import pymysql
import pymongo
import datetime
from bson import ObjectId

client = pymongo.MongoClient('mongodb://root:Baiguan2016@60.205.152.167:3717')
database = client.shengjian
print(str(datetime.date.today()))
# col = database.store_list.find({'ts_string': '2017-06-01', 'latitude': {'$ne': None}}).limit(10)
# s = {}
col = database.store_list.find({'_id':ObjectId('592f752882e0165f3cfcb1f9')},{'id':1,'name':1,'address':1,'city':1,'category':1,'recent_order_num':1,
                                                                                  'float_minimum_order_amount':1,'ts_string':1,'rating':1,
                                                                                  'float_delivery_fee':1,'delivery_mode':1,'activities':1,'ts':1,'_id':0})
s = {}
c = 0
for ite in col:
    if c % 10000 == 0:
        print('count', c)
    c += 1
    try:
        s[ite['id']] = ite
    except:
        print(ite)
l = list(s.values())
c = 0
for item in l:
    if c % 10000 == 0:
        print('count', c)
    c += 1
    store_id = item.get('id', '')
    if not store_id:
        continue
    try:
        name = item.get('name', '')
        address = item.get('address', '')
        city = item.get('city', '')
        category = item.get('category', '')
        month_sale = item.get('recent_order_num', 0)
        min_price = item.get('float_minimum_order_amount', 0)
        score = item.get('rating', 0)
        delivery_fee = item.get('float_delivery_fee', 0)
        delivery_type = 2 if '准时达' in [x.get('name', '') for x in item.get('supports', []) if
                                       item.get('supports', [])] else (
            item.get('delivery_mode', '').get('id', 0) if item.get('delivery_mode', '') else 0)

        delivery_name = '准时达' if '准时达' in [x.get('name', '') for x in item.get('supports', []) if
                                           item.get('supports', [])] else (
            item.get('delivery_mode', '').get('text', '') if item.get('delivery_mode', '') else '')

        is_promotion = 1 if item.get('activities', '') else 0
        promotion_type = '|'.join([str(i.get('type', '')) for i in item.get('activities', '')]) if is_promotion else ''
        promotion_name = '|'.join([i.get('tips', '') for i in item.get('activities', '')]) if is_promotion else ''
        ts = item['ts']
        ts_string = item['ts_string']
        source = 2
        print(delivery_type, delivery_name, 111)
        if delivery_type==2:
            print(item)
    except:
        print(item['_id'])
