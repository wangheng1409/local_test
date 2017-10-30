import pymongo
from datetime import timedelta, date
from bo_lib.general import BONotifier
from collections import defaultdict
from pybloom import BloomFilter
import time

st=time.time()
yesterstoday=date.today() - timedelta(days=1)
yesterstoday_yesterstoday=date.today() - timedelta(days=2)
t=[yesterstoday_yesterstoday,yesterstoday]

client = pymongo.MongoClient('mongodb://root:Baiguan2016@dds-2ze4486117714fa42.mongodb.rds.aliyuncs.com:3717,dds-2ze4486117714fa41.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-2719521')
database = client.shengjian
print(str(date.today()))
ss=[]
yesterstoday_store_set=''
for i in t:
    s=set()
    f = BloomFilter(capacity=100000*100000, error_rate=0.0001)
    f.FILE_FMT
    col = database.store_list.find({'ts_string': str(i),'latitude':{'$ne':None}}, {'id': 1})
    c = 0
    for item in col:
        if c % 10000 == 0:
            print(i,'count', c)
        c += 1
        try:
            if item['id'] not in f:
                f.add(item['id'])
                s.add(item['id'])
        except:
            print(item)

    l = len(f)
    ss.append(l)

    if i==yesterstoday:
        yesterstoday_store_set=s

print('start_all')


f1 = BloomFilter(capacity=100000*100000, error_rate=0.0001)
f2= BloomFilter(capacity=100000*100000, error_rate=0.0001)

i = 1
while True:
    day = str(date.today() - timedelta(days=i))
    if day < '2017-05-20':
        break
    col = database.store_list.find({'latitude': {'$ne': None}, 'ts_string': day},{'id':1})
    c = 0
    for ite in col:
        if c % 10000 == 0:
            print(day,'all', c)
        c += 1
        try:
            f1.add(ite['id'])
            if i>1:
                f2.add(ite['id'])
        except Exception as e:
            print(e)
    i += 1
l1 = len(f1)
ss.append(l1)
l2=len(f2)
ss.append(l2)


#all category
f3 = BloomFilter(capacity=100000*100000, error_rate=0.0001)
s={}
city_num=defaultdict(int)
category_num=defaultdict(int)
i = 1
while True:
    day = str(date.today() - timedelta(days=i))
    if day < '2017-05-20':
        break
    col = database.store_list.find({'ts_string': str(day),'latitude':{'$ne':None}}, {'id': 1})
    c = 0
    for item in col:
        if c % 10000 == 0:
            print(i,'count', c)
        c += 1
        try:
            if item['id'] not in f3:
                f3.add(item['id'])
                s[item['id']] = item
        except:
            print(item)
l=list(s.values())
for item in l:
    if item.get('city',''):
        city_num[item['city']]+=1
        category_num[item['category']]+=1

print(city_num,category_num)

item1=ss[1]
item2=ss[1]-ss[0]
item3=len(list(set(list(f1))-set(list(f2))))
item4=category_num
item5=ss[2]
all_time=time.time()-st
print(all_time)
print('item1:',item1,'\nitem2',item2,'\nitem3',item3,'\nitem4',item4,'\nitem5',item5,)
# BONotifier.msg('SJ QA Table of %s\n'
#                'Num of Poi crawled on %s:%s\n'
#                'Increase Num of Poi crawled from %s to %s:%s\n'
#                'Num of New Poi crawled on yesterday:%s\n'
#                'Num of Poi by Category:%s\n'
#                'Num of Total Poi:%s\n'
#                % (str(yesterstoday),
#                   str(yesterstoday),item1,
#                   str(yesterstoday_yesterstoday),str(yesterstoday),item2,
#                   item3,
#                   item4,
#                   item5
#                   ))
