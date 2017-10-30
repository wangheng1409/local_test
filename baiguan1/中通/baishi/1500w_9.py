# !/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import redis
import pymysql

all_oid=100*10000
oid_list_9=[605,606,607,608,609,650]
ran_list_9 = [74398, 52843, 4598, 1120, 186, 16037]
oid_list_12=[210,211,217,220,224,240,250,280,281,310,350,356,610,630,660,667]
ran_list_12=[95,11155,1,1805,1,143,199,5306,1,17,6642,2,765,26,6,10]
def get_oidnum_dic():
    gailv_9=[int(x/sum(ran_list_9)*0.75*all_oid) for x in ran_list_9]
    gailv_12=[int(x/sum(ran_list_12)*0.15*all_oid) for x in ran_list_12]

    oid_9_dic={}
    for k,v in zip(oid_list_9,gailv_9):
        oid_9_dic[str(k)]=v

    oid_12_dic = {}
    for k, v in zip(oid_list_12, gailv_12):
        oid_12_dic[str(k)] = v

    return oid_9_dic,oid_12_dic

def get_max_oid():
    # 创建连接
    conn = pymysql.connect(host='101.201.120.75', port=3306, user='writer', passwd='Bigone2017', db='zto',
                           charset='utf8')
    # 创建游标
    cursor = conn.cursor()
    cursor.execute('''select len_oid, start_oid, max(oid) as max_oid
                    from
                    (
                    select  oid, substr(oid,1,3) as start_oid, length(oid) as len_oid
                    from baishi_detail
                    where raw != ''
                    and task_id in ('test_baishi_9', 'test_baishi_12') and substr(dt,1,10)<'2017-09-20'
                    ) t
                    group by len_oid, start_oid
                    order by len_oid, start_oid''')
    ret = cursor.fetchall()
    max_oid_9={}
    max_oid_12={}
    for item in ret:
        if item[0]==9:
            max_oid_9[str(item[1])]=int(item[2])
        elif item[0]==12:
            max_oid_12[str(item[1])] = int(item[2])

    return max_oid_9,max_oid_12

oid_9_dic, oid_12_dic=get_oidnum_dic()

max_oid_9,max_oid_12=get_max_oid()

print( oid_9_dic,max_oid_9)
# print(oid_9_dic, oid_12_dic,max_oid_9,max_oid_12)

pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db='0')
r = redis.Redis(connection_pool=pool)
# k='baishi_test_1500w_9'
# for key,max_oid in max_oid_9.items():
#     for i in range(max_oid,max_oid+oid_9_dic[key]):
#         r.lpush(k,json.dumps(i))
k1="baishi_test_1500w_12"
for key,max_oid in max_oid_12.items():
    for i in range(max_oid,max_oid+oid_12_dic[key]):
        r.sadd(k1,json.dumps(i))

    print(key)