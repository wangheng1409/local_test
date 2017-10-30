# !/usr/bin/env python
# -*- coding:utf-8 -*-


from datetime import timedelta, date
import pymongo
import redis
import json

city_list=['北京','上海','广州','深圳',
           '沈阳','济南','杭州','南京','合肥','太原','福州','长沙','成都','石家庄',
           '惠州','泉州','宜昌','开封','南通','金华',]

client = pymongo.MongoClient('mongodb://root:Baiguan2016@dds-2ze4486117714fa42.mongodb.rds.aliyuncs.com:3717,dds-2ze4486117714fa41.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-2719521')
database = client.shengjian
db1 = client['Meituan']['lng-lat']

ss_all = set()
ss_yesterday_yesterday = set()
i = 1
while True:
    day = str(date.today() - timedelta(days=i))
    if day < '2017-05-20':
        break
    if day>'2017-06-01':
        continue
    if day=='2017-05-31':
        continue
    col = database.store_list.find({'latitude': {'$ne': None}, 'ts_string': day},{'id':1,'area_name':1,'city':1,'_id':0})
    c = 0
    for ite in col:
        if c % 10000 == 0:
            print(day,'all', c)
        c += 1
        try:
            if ite['city'] not in city_list:
                continue
            if day>'2017-05-24' and day<'2017-06-03':
                ss_all.add(ite['area_name'])
            if day<'2017-05-25':
                ss_yesterday_yesterday.add(ite['area_name'])
        except Exception as e:
            print(e)
    i += 1

ret=list(ss_yesterday_yesterday-ss_all)

pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db='0', password='bigone2016')
r = redis.Redis(connection_pool=pool)
key='storelistspiderbycategory'
print('未抓取到的小区数',len(ret))

c=0
for item in ret:
    if c % 100 == 0:
        print('store_id_num', c)
    c += 1
    r.lpush(key,json.dumps(db1.find_one({'name': item},{'_id':0})))

