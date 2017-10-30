import pymongo
import json
import redis
from datetime import timedelta, date
client=pymongo.MongoClient('mongodb://root:Baiguan2016@60.205.152.167:3717')
database=client.shengjian

ss_all = set()
i = 1
while True:
    day = str(date.today() - timedelta(days=i))
    if day < '2017-06-04':
        break
    col = database.store_list.find({'latitude': {'$ne': None}, 'ts_string': day},{'id':1,'latitude':1,'longitude':1,'_id':0})
    c = 0
    for ite in col:
        if c % 10000 == 0:
            print(day,'all', c)
        c += 1
        # print(ite)
        try:
            ss_all.add(json.dumps(ite))
        except Exception as e:
            print(e)
    i += 1

pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db='0')
r = redis.Redis(connection_pool=pool)
for i in ss_all:
    r.rpush('ele_store_id', i)