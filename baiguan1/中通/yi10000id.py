import redis
import pandas as pd
import random
# #
id_pd = pd.read_csv('jdwl_10000.csv', header=0, sep=',')
# print(id_pd)
s=id_pd['oid'].values.tolist()
# print(s)
oid_list=s

# def oid_generator():
#     # res = se.INITIAL+"%0.10d" % random.randint(0,9999999999)
#     # res = "%0.12d" % random.randint(0, 999999999999)
#     res = random.choice(['3', '4', '5', '6']) + "%0.10d" % random.randint(0, 9999999999)
#     if len(str(int(res))) < 11:
#         return oid_generator()
#     else:
#         return res
# oid_list=[oid_generator() for i in range(10000)]

#
# pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db='0', password='bigone2016')
pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db='0')
r = redis.Redis(connection_pool=pool)
k=str(0)
print(len(oid_list))
for oid in oid_list:
    r.sadd('jd1',oid)

# import pymongo
# client=pymongo.MongoClient('mongodb://root:Baiguan2016@60.205.152.167:3717')
# database=client.new_zto
# col=database.zto_detail.find({'source':'zto','raw':{'$exists':1}},{'_id':0,'oid':1}).limit(10000)
# oid_list=[]
# for item in col:
#     oid_list.append(item['oid'])
# # print(oid_list)
# #
# id_pd = pd.read_csv('zto_order.csv', header=0, sep=',')
# # print(id_pd)
# s=id_pd['oid'].values.tolist()
# # print(s)
# oid_list=s
# import pymongo
# client=pymongo.MongoClient()
# database=client.new_zto
# col=database.zto_detail.distinct('oid',{'source':'zto','raw':{'$exists':1}})
# # col1=database.zto_detail.distinct('oid',{'source':'baidu'})
# s=set()
# t=set(oid_list)
# for i in col:
#     s.add(int(i))
#
# ss=t-s
# print(len(ss),ss)

