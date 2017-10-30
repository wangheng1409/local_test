# !/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import redis
import pymongo
client = pymongo.MongoClient()
collection = client.new_zto.baishi_detail

col=collection.distinct('oid',{'task_id':'baishi_test_10w'})
s=set()
t=set()
for i in col:
    s.add(i)

for i in range(211332004011,211332004011+10*10000):
    t.add(str(i))

ret=t-s
print(len(ret),len(s),len(t))
# print(s)



pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db='0')
r = redis.Redis(connection_pool=pool)
k='baishi_test_10w'
for i in ret:
    r.sadd(k,i)