import pymongo
import datetime
from datetime import timedelta, date
from collections import defaultdict

client = pymongo.MongoClient('mongodb://root:Baiguan2016@dds-2ze4486117714fa42.mongodb.rds.aliyuncs.com:3717,dds-2ze4486117714fa41.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-2719521')
database = client.Meituan
db1=client.monitor.detail
print(str(date.today()))
start_day=datetime.datetime(2017,5,24).date()
yesterday=str(date.today() - timedelta(days=1))

i=0
while True:
    day = str(start_day + timedelta(days=i))
    if day > yesterday:
        break
    if db1.find_one({'ts_string':day,'source':'ky'}):
        i+=1
        continue
    #all category
    col=database.POI_LATEST_BY_SHORT.find({'ts_string':day},{'id':1,'city':1})
    s={}
    city_num=defaultdict(int)
    c = 0
    for item in col:
        if c % 10000 == 0:
            print('count', c)
        c+=1
        try:
            s[item['id']]=item
        except:
            print(item)
    l=list(s.values())
    for item in l:
        if item.get('city',''):
            city_num[item['city']]+=1

    print(city_num)
    city_num['全部']=len(l)
    ss={
        'source':'ky',
        'ts_string':day,
        'data':city_num,
    }

    db1.insert(ss)
    i+=1