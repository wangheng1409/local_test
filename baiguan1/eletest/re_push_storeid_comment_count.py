# !/usr/bin/env python
# -*- coding:utf-8 -*-
import pymysql
import pymongo
import datetime
import  redis
import json
from datetime import timedelta, date

client = pymongo.MongoClient(
    'mongodb://root:Baiguan2016@dds-2ze4486117714fa42.mongodb.rds.aliyuncs.com:3717,dds-2ze4486117714fa41.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-2719521')
database = client.shengjian


ss_all = set()
i = 1
while True:
    day = str(date.today() - timedelta(days=i))
    if day < '2017-05-20':
        break
    col = database.store_list.find({'latitude': {'$ne': None}, 'ts_string': day},{'id':1})
    c = 0
    for ite in col:
        if c % 10000 == 0:
            print(day,'all', c)
        c += 1
        try:
            ss_all.add(ite['id'])
        except Exception as e:
            print(e)
    i += 1

comment=database.store_comment_count
comment_store_id=comment.distinct('store_id')
ret=ss_all-set(comment_store_id)

pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db='0', password='bigone2016')
r = redis.Redis(connection_pool=pool)
key='commentcountspider'
print('未抓取到的店铺数',len(ret))
c=0
for item in ret:
    if c % 10000 == 0:
        print('store_id_num', c)
    c += 1
    store_id=item
    store_dict_list=database.store_list.find({'id':store_id},{'id':1,'latitude':1,'longitude':1,'_id':0})
    store_dict=[x for x in store_dict_list][0]
    r.lpush(key,json.dumps(store_dict))

