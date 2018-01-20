# !/usr/bin/env python
# -*- coding:utf-8 -*-
import redis
import pymongo
import json



REDIS_HOST = '10.9.99.34'
REDIS_PORT = 6379
REDIS_PARAMS = {'password': 'bigone2016'}
REDIS_PASSWORD = 'bigone2016'

host = REDIS_HOST
port = REDIS_PORT
password = REDIS_PASSWORD
client = redis.StrictRedis(host=host, port=port, password=password)

mongocli = pymongo.MongoClient('mongodb://root:big_one_112358@123.59.69.66:5600')
collection = mongocli.ebay.ebay_us_category_cut
for item in collection.find({},{'_id':0,'ts':0}):
    client.lpush('ebay_us',json.dumps(item))