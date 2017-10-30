import pymongo
import datetime,time
from collections import defaultdict
client=pymongo.MongoClient('mongodb://root:Baiguan2016@60.205.152.167:3717')
database=client.shengjian
print(str(datetime.date.today()))
# col=database.store_list.find({'ts_string':str(datetime.date.today())},{'id':1,'city':1,'category':1})
col=database.store_list.find({'ts_string':{'$gte':'2017-05-24'}},{'id':1,'city':1,'category':1})
s={}
city_num={}


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
    if item['city'] not in city_num:
        city_num[item['city']]=defaultdict(int)
    city_num[item['city']][item['category']]+=1

print(city_num)

# f=open('city_category_storenum_2017_05_31.csv','w')
# f.close()
# with open('city_category_storenum_2017_05_31.csv','r+') as f1:
#     for city,category in city_num.items():
#         for k,v in category.items():
#             f1.write('\t'.join([city,k,str(v)])+'\n')
s={}
for k,v in city_num.items():
    s[k]=sum(v.values())
print(s)