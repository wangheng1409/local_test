# !/usr/bin/env python
# -*- coding:utf-8 -*-
import pymysql
import pymongo
import datetime
from datetime import timedelta, date
import time


def detil(l):
    c = 0
    for item in l:
        if c % 10000 == 0:
            print('count1', c)
            if c!=0:
                conn.commit()
        c += 1
        store_id = item.get('id', '')
        if not store_id:
            continue
        if store_id in ss:
            continue
        try:
            ss.add(store_id)
            name = item.get('name', '')
            address = item.get('address', '')
            city = item.get('city', '')
            category = item.get('category', '')
            month_sale = item.get('recent_order_num', 0) if item.get('ts_string', '1970-01-01') >= str(
                lastweek) else None
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
            promotion_type = '|'.join(
                [str(i.get('type', '')) for i in item.get('activities', '')]) if is_promotion else ''
            promotion_name = '|'.join([i.get('tips', '') for i in item.get('activities', '')]) if is_promotion else ''
            ts = item['ts']
            ts_string = item['ts_string']
            insert_ts = str(today)
            source = 2


            # 执行SQL，并返回受影响行数
            effect_row = cursor.execute(
                "insert into waimai_poi(poi_id,poi_name,poi_address,city,category,month_sale,min_price,"
                "score,delivery_fee,delivery_type,delivery_name,is_promotion,promotion_type,promotion_name,"
                "source,ts,ts_string,insert_ts)"
                "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (store_id, name, address,
                                                                                  city, category, month_sale, min_price,
                                                                                  score, delivery_fee, delivery_type,
                                                                                  delivery_name,
                                                                                  is_promotion, promotion_type,
                                                                                  promotion_name, source, ts, ts_string,
                                                                                  insert_ts))

        except Exception as e:
            print(e, 111)

    conn.commit()
t = time.time()

today = date.today()
lastweek = date.today() - timedelta(days=7)
# 创建连接
conn = pymysql.connect(host='101.201.120.75', port=3306, user='writer', passwd='Bigone2017', db='kysj', charset='utf8')
# 创建游标
cursor = conn.cursor()

client = pymongo.MongoClient('mongodb://root:Baiguan2016@dds-2ze4486117714fa42.mongodb.rds.aliyuncs.com:3717,dds-2ze4486117714fa41.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-2719521')
database = client.shengjian
print(str(datetime.date.today()))
ss = set()
i = 1
while True:
    day = str(date.today() - timedelta(days=i))
    if day < '2017-05-25':
        break
    col = database.store_list.find({'latitude': {'$ne': None}, 'ts_string': day},{'id':1,'name':1,'address':1,'city':1,'category':1,'recent_order_num':1,
                                                                                  'float_minimum_order_amount':1,'ts_string':1,'rating':1,
                                                                                  'float_delivery_fee':1,'delivery_mode':1,'supports':1,'activities':1,'ts':1,'_id':0})
    s = {}
    c = 0
    for ite in col:
        if c % 10000 == 0:
            print('count', c)
        c += 1
        try:
            s[ite['id']] = ite
        except Exception as e:
            print(e)
    detil(list(s.values()))
    i += 1

# 关闭游标
cursor.close()
# 关闭连接
conn.close()
print(time.time() - t)



