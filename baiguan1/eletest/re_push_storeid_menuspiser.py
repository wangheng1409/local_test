# !/usr/bin/env python
# -*- coding:utf-8 -*-
import pymysql
import pymongo
import datetime
import  redis
import json
# 创建连接
conn = pymysql.connect(host='101.201.120.75', port=3306, user='writer', passwd='Bigone2017', db='kysj',charset='utf8')
# 创建游标
cursor = conn.cursor()
cursor.execute("select poi_id from waimai_poi where source=2 and insert_ts='2017-07-21'  and `gmv` is null and `ts_string`>'2017-07-13'")
ret=cursor.fetchall()

client = pymongo.MongoClient(
    'mongodb://root:Baiguan2016@dds-2ze4486117714fa42.mongodb.rds.aliyuncs.com:3717,dds-2ze4486117714fa41.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-2719521')
database = client.shengjian


conn.commit()

pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db='0', password='bigone2016')
r = redis.Redis(connection_pool=pool)
key='menuspider'
print('未抓取到的店铺数',len(ret))
c=0
for item in ret:
    if c % 100 == 0:
        print('store_id_num', c)
    c += 1
    store_id=item[0]
    store_dict_list=database.store_list.find({'id':store_id},{'id':1,'latitude':1,'longitude':1,'_id':0})
    store_dict=[x for x in store_dict_list][0]
    r.lpush(key,json.dumps(store_dict))

# 关闭游标
cursor.close()
# 关闭连接
conn.close()