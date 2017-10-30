# !/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime, time
import pymysql
import pymongo
import redis
from collections import defaultdict
from datetime import timedelta, date
lastweek=date.today() - timedelta(days=5)


# 创建连接
conn = pymysql.connect(host='101.201.120.75', port=3306, user='writer', passwd='Bigone2017', db='kysj', charset='utf8')
# 创建游标
cursor = conn.cursor()

cursor.execute("select poi_id from waimai_poi where source=2 and insert_ts='2017-07-27'  and gmv is  null ")
ret=cursor.fetchall()

# client = pymongo.MongoClient(
#     'mongodb://root:Baiguan2016@dds-2ze4486117714fa42.mongodb.rds.aliyuncs.com:3717,dds-2ze4486117714fa41.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-2719521')
client=pymongo.MongoClient('mongodb://root:Baiguan2016@60.205.152.167:3717')
database = client.shengjian


c=0
for item in ret:
    if c % 100 == 0:
        print('store_id_num', c)
    c += 1
    store_id=item[0]
    store_dict_list=database.store_list.find({'id':store_id},{'id':1,'name':1,'address':1,'city':1,'category':1,'recent_order_num':1,
                                                                                  'float_minimum_order_amount':1,'ts_string':1,'rating':1,
                                                                                  'float_delivery_fee':1,'delivery_mode':1,'supports':1,'activities':1,'ts':1,'_id':0})

    item=[x for x in store_dict_list][-1]
    month_sale = item.get('recent_order_num', 0) if item.get('ts_string', '1970-01-01') >= str(
                '2017-07-13') else None
    cursor.execute('update waimai_poi set month_sale=%s  where poi_id=%s and source=2 and insert_ts=%s ',
                           (month_sale, store_id, '2017-07-21'))
    conn.commit()
# 关闭游标
cursor.close()
# 关闭连接
conn.close()
