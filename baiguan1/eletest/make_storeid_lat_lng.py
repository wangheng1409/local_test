# !/usr/bin/env python
# -*- coding:utf-8 -*-

import pymongo
from bson import ObjectId
client = pymongo.MongoClient(
    'mongodb://root:Baiguan2016@dds-2ze4486117714fa42.mongodb.rds.aliyuncs.com:3717,dds-2ze4486117714fa41.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-2719521')
database = client.shengjian
w=database.storeid_lat_lng
ss=set()
last_id=ObjectId("5920010982e016361229fcfd")
all_num = database.store_list.count()
c=0
while c<all_num+10000:
    if c % 10000 == 0:
        print('store_id_num', c)

    col=database.store_list.find({'_id': {'$gte': last_id},'latitude':{'$ne':None}},{'id':1,'latitude':1,'longitude':1,'_id':1}).limit(10000)
    col=[x for x in col]
    for item in col:
        try:
            if item['id'] not in ss:
                ss.add(item['id'])
                w.insert(item)
        except:
            print(item['_id'])

    if len(col)>0:
        last_id = col[-1]['_id']
        c += 10000
    else:
        break

