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
cursor.execute("select poi_id from waimai_poi where source=2 and insert_ts='2017-07-27'  and gmv is  null")
ret=cursor.fetchall()
s=set()
for item in ret:
    s.add(item['poi_id'])



conn.commit()
# 关闭游标
cursor.close()
# 关闭连接
conn.close()


client = pymongo.MongoClient(
    'mongodb://root:Baiguan2016@dds-2ze4486117714fa42.mongodb.rds.aliyuncs.com:3717,dds-2ze4486117714fa41.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-2719521')
database = client.shengjian

pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db='0', password='bigone2016')
r = redis.Redis(connection_pool=pool)

store_dict_list=database.store_list.distinct('id',{'ts_string':'2017-06-02'})
ss=set(store_dict_list)
print(len(list(s-ss)),s-ss)



