# !/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime, time
import pymysql
import pymongo
import redis
from collections import defaultdict
import json
from datetime import timedelta, date
lastweek=date.today() - timedelta(days=7)
print(lastweek)
from odps import ODPS, options
options.limited_instance_tunnel = False
o = ODPS('LTAIxrZjJRgoUked', 'RZKFDNUyScX9TX6UH2xJJmMsnwlfJ4',
   project='kysj')

s=set()
with o.execute_sql('select poi_id from sj_menu where ts_string>"2017-07-18" group by poi_id').open_reader() as reader:
    c=0
    for item in reader:
        # print(item['poi_id'],item['gmv'])
        if c % 10000 == 0:
            print('store_id_num', c)
        c += 1
        s.add(item['poi_id'])

t=set()
pool = redis.ConnectionPool(host='60.205.152.167', port='6379', db='0',password='bigone2016')
r = redis.Redis(connection_pool=pool)
id_list=r.lrange('ele_store_id',0,-1)
for ids in id_list:
    l_dict=json.loads(ids.decode())
    t.add(l_dict['id'])
w=t-s
for i in w:
    r.lpush('menuspider', i)

# print(t)

