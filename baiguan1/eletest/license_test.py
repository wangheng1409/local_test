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


t = set()
i = 0
while True:
    day = str(date.today() - timedelta(days=i))
    if day < '2017-06-04':
        break
    col = database.store_license.find({ 'ts_string': day},{'_id': 1, 'store_id': 1, 'license': 1}).limit(5)
    for item in col:
        print(item['license'])
        store_id = item['store_id']
        if item['license'] == True:
            lic = 1
        else:
            lic = 0
        try:
            print(lic,555)
            cursor.execute('update waimai_poi set is_certificated=%s where poi_id=%s and source=2 and insert_ts>%s ',
                           (lic, store_id, lastweek))
            conn.commit()
        except Exception as e:
            print(e, '更新失败', store_id)

    i += 1


# 关闭游标
cursor.close()
# 关闭连接
conn.close()
