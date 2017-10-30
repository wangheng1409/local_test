# !/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime, time
import pymysql
import pymongo
import redis
from collections import defaultdict
from datetime import timedelta, date
lastweek=date.today() - timedelta(days=7)


def object_id(day, hour):
    from bson import ObjectId
    return ObjectId(str(hex(int(time.time() - 86400 * day - 3600 * hour))[2:]) + 16 * '0')

def detil(l):
    global t
    total = defaultdict(int)
    c = 0
    for food in l:
        if c % 10000 == 0:
            print('menu_id_num', c)
        c += 1
        if food.get('item_id', ''):
            if food.get('item_id', '') in t:
                continue
            else:
                t.add(food.get('item_id', ''))
            food_month_sale_num = food['month_sales']
            if food.get('specfoods', []):
                ss = 0
                for i in food['specfoods']:
                    ss += (i['price'] + i['packing_fee'])
                price = float(ss) / len(food['specfoods'])
                if price <= 1500:
                    total[food['store_id']] += food_month_sale_num * price

    c = 0
    for store_id, food_list in total.items():
        if c % 10000 == 0:
            print('store_id_num1', c)
        c += 1

        store_month_sale = food_list
        try:
            cursor.execute('update waimai_poi set gmv=%s where poi_id=%s and source=2 and insert_ts>%s ',
                       (store_month_sale, store_id, lastweek))
        except Exception as e:
            print(e,'更新失败',store_id)

        conn.commit()

# 创建连接
conn = pymysql.connect(host='101.201.120.75', port=3306, user='writer', passwd='Bigone2017', db='kysj', charset='utf8')
# 创建游标
cursor = conn.cursor()

client = pymongo.MongoClient(
    'mongodb://root:Baiguan2016@dds-2ze4486117714fa42.mongodb.rds.aliyuncs.com:3717,dds-2ze4486117714fa41.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-2719521')
database = client.shengjian


t = set()
i = 0
while True:
    day = str(date.today() - timedelta(days=i))

    col = database.store_menu_list.find({ 'ts_string': day},{'_id': 1, 'store_id': 1, 'item_id': 1, 'specfoods': 1,
                                         'month_sales': 1, })

    # s = {}
    # c = 0
    # for ite in col:
    #     if c % 10000 == 0:
    #         print('count', c)
    #     c += 1
    #     try:
    #         s[ite['item_id']] = ite
    #     except Exception as e:
    #         print(e)
    detil(col)
    break


# 关闭游标
cursor.close()
# 关闭连接
conn.close()
