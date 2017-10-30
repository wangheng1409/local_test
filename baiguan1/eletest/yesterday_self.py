# !/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime, time
import pymysql
import pymongo
import redis
from collections import defaultdict
from datetime import timedelta, date




yesterstoday=date.today() - timedelta(days=0)
yesterstoday_yesterstoday=date.today() - timedelta(days=1)
t=[yesterstoday_yesterstoday,yesterstoday,]

yesterstoday_yesterstoday_set=''
yesterstoday_set=''

client = pymongo.MongoClient(
    'mongodb://root:Baiguan2016@60.205.152.167:3717')
database = client.shengjian
for i in t:
    col = database.store_list.find({'ts_string': str(i),'latitude':{'$ne':None}}, {'id': 1})
    col = [x for x in col]
    print(col[0])
    s = {}
    c = 0
    for item in col:
        if c % 10000 == 0:
            print('count', c)
        c += 1
        try:
            s[item['id']] = item
        except:
            print(item)
    if i==yesterstoday:
        yesterstoday_set=set(s.keys())
    else:
        yesterstoday_yesterstoday_set=set(s.keys())

print(yesterstoday_yesterstoday_set-yesterstoday_set)