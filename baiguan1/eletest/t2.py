import pymongo
import datetime,time
from collections import defaultdict

client=pymongo.MongoClient('mongodb://root:Baiguan2016@60.205.152.167:3717')
database=client.shengjian
print(str(datetime.date.today()))
# col=database.store_list.find({'ts_string':str(datetime.date.today())},{'id':1,'city':1,'category':1})
col=database.store_list.find({'ts_string':'2017-05-24'},{'id':1,'city':1,'category':1})
s={}
city_num=defaultdict(int)
category_num=defaultdict(int)

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
    city_num[item['city']]+=1
    category_num[item['category']]+=1

print(city_num,category_num)

# menu=database.store_menu_list.find({'ts_string':str(datetime.date.today())}).count()



