# !/usr/bin/env python
# -*- coding:utf-8 -*-


from datetime import timedelta, date
import pymongo


uri = 'mongodb://root:Baiguan2016@dds-2ze4486117714fa42.mongodb.rds.aliyuncs.com:3717,dds-2ze4486117714fa41.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-2719521'
mongo = pymongo.MongoClient(uri)
db1 = mongo['Meituan']['lng-lat']
db = mongo['shengjian']['store_list']


i = 7
while True:
    day = str(date.today() - timedelta(days=i))
    if day < '2017-05-20':
        break
    col = db.find({'latitude': {'$ne': None}, 'ts_string': day,'fixed':{'$exists':False}},{'latitude':1,'longitude':1,'area_name':1},no_cursor_timeout=True)
    print('CNT:', col.count())
    c = 0
    urls = []
    ids = []
    for doc in col:
        if c % 10000 == 0:
            print(day,'all', c)
        c += 1
        try:
            area_name=doc['area_name']
            city=db1.find_one({ 'name': area_name })['city']
            db.update_one(
                {'_id': doc['_id']},
                {'$set': {
                    "city": str(city),
                    'fixed': 1,
                    'latitude': str(doc['latitude']),
                    'longitude': str(doc['longitude']),
                }}
            )

            # print('fin')
        except Exception as e:
            print(e)
    col.close()
    i += 1
