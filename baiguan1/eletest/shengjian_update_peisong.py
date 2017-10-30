# !/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime, time
import pymysql
import pymongo
import redis
from collections import defaultdict
from datetime import timedelta, date
lastweek=date.today() - timedelta(days=7)

# 创建连接
conn = pymysql.connect(host='101.201.120.75', port=3306, user='writer', passwd='Bigone2017', db='kysj', charset='utf8')
# 创建游标
cursor = conn.cursor()

client = pymongo.MongoClient(
    'mongodb://root:Baiguan2016@60.205.152.167:3717')
database = client.shengjian


cursor.execute('select poi_id from waimai_poi where source=2 and insert_ts="2017-06-01"')
ret=cursor.fetchall()
conn.commit()
t = set()
i = 1
c=0
for poi in ret:
    if c % 1000 == 0:
        print('store_id_num', c)
    c += 1
    poi_id=poi[0]
    item = database.store_list.find_one({'id':int(poi_id) },
                                   {'delivery_mode': 1, 'supports': 1})

    delivery_type = 2 if '准时达' in [x.get('name', '') for x in item.get('supports', []) if
                                   item.get('supports', [])] else (
        item.get('delivery_mode', '').get('id', 0) if item.get('delivery_mode', '') else 0)

    delivery_name = '准时达' if '准时达' in [x.get('name', '') for x in item.get('supports', []) if
                                       item.get('supports', [])] else (
        item.get('delivery_mode', '').get('text', '') if item.get('delivery_mode', '') else '')

    cursor.execute('update waimai_poi set delivery_type=%s where poi_id=%s and source=2 and insert_ts=%s', (delivery_type, poi_id,'2017-06-01'))
    cursor.execute('update waimai_poi set delivery_name=%s where poi_id=%s and source=2 and insert_ts=%s', (delivery_name, poi_id,'2017-06-01'))
    conn.commit()


# 关闭游标
cursor.close()
# 关闭连接
conn.close()
