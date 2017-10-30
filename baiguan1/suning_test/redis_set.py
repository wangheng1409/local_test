# !/usr/bin/env python
# -*- coding:utf-8 -*-
import redis

pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db='0', password='bigone2016')
r = redis.Redis(connection_pool=pool)
s=set()
for item in r.lrange('suning_store_id',0,-1):
    s.add(item)

print(len(s))
r.delete('suning_store_id')
for item in s:
    r.lpush('suning_store_id',item)

