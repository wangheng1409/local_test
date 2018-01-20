# !/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime, time
import pymysql
import pymongo
import redis
from collections import defaultdict
from datetime import timedelta, date
lastweek=date.today() - timedelta(days=3)

sss=set()

def detil(l):
    global t
    total = defaultdict(int)
    will_toya=defaultdict(list)
    c = 0
    for food in l:
        if not food.get('store_id',''):
            continue
        if not food.get('item_id',''):
            continue
        if not food.get('month_sales', ''):
            continue

        will_toya[food['item_id']].append(food['store_id'])
        if c % 10000 == 0:
            print('menu_id_num', c)
        c += 1
        if food.get('item_id', ''):
            will_toya[food['item_id']].append(food['name'])
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
                if price > 1500:
                    sss.add(food.get('store_id',''))
                else:
                    total[food['store_id']] += food_month_sale_num * price

                will_toya[food['item_id']].append(food['month_sales'])
                will_toya[food['item_id']].append(price)

                if len(will_toya[food['item_id']])!=4:
                    print(will_toya[food['item_id']])
    print(sss)
    # print(total)
    # print(will_toya)
    f=open('ele_2017-11-30.csv','a+')
    f.close()
    with open('ele_2017-11-30.csv','a+',encoding='utf8') as f:
        for k,v in will_toya.items():
            store_id=v[0]
            name=v[1]
            month_sales=v[2]
            price=v[3]
            f.write('|'.join([str(x) for x in [k,store_id,name,month_sales,price]])+'\n')


    # c = 0
    # for store_id, food_list in total.items():
    #     if c % 10000 == 0:
    #         print('store_id_num', c)
    #     c += 1
    #
    #     store_month_sale = food_list
    #     try:
    #         cursor.execute('update waimai_poi set gmv=%s where poi_id=%s and source=2 and insert_ts>%s ',
    #                    (store_month_sale, store_id, lastweek))
    #     except Exception as e:
    #         print(e,'更新失败',store_id)
    #
    #     conn.commit()

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
    if day < '2017-11-28':
        break
    col = database.store_menu_list.find({ 'ts_string': day},{'_id': 1, 'store_id': 1, 'item_id': 1,'name': 1, 'specfoods': 1,
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
    i += 1


# 关闭游标
cursor.close()
# 关闭连接
conn.close()
print(sss)
