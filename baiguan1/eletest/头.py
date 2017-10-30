import pymongo
from datetime import timedelta, date
from bo_lib.general import BONotifier
from collections import defaultdict

yesterstoday=date.today() - timedelta(days=1)
yesterstoday_yesterstoday=date.today() - timedelta(days=2)
t=[yesterstoday_yesterstoday,yesterstoday,'all']

client = pymongo.MongoClient('mongodb://root:Baiguan2016@dds-2ze4486117714fa42.mongodb.rds.aliyuncs.com:3717,dds-2ze4486117714fa41.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-2719521')
database = client.shengjian
print(str(date.today()))
ss=[]
yesterstoday_store_set=''
all_store_set=''
for i in t:
    if i=='all':
        col = database.store_list.find({'latitude':{'$ne':None}}, {'id': 1})
    else:
        col = database.store_list.find({'ts_string': str(i),'latitude':{'$ne':None}}, {'id': 1})
    col = [x for x in col]
    print(col[0])
    s = {}
    c = 0
    for item in col:
        if c % 10000 == 0:
            print('count', c)
        c += 1
        try:
            s[item['id']] = item
        except:
            print(item)

    l = len(list(s.keys()))
    ss.append(l)

    if i==yesterstoday:
        yesterstoday_store_set=set(list(s.keys()))
    elif i=='all':
        all_store_set=set(list(s.keys()))

#all category
col=database.store_list.find({'latitude':{'$ne':None}},{'id':1,'city':1,'category':1})
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
    if item.get('city',''):
        city_num[item['city']]+=1
        category_num[item['category']]+=1

print(city_num,category_num)

item1=ss[1]
item2=ss[1]-ss[0]
item3=len(list(yesterstoday_store_set-all_store_set))
item4=category_num
item5=ss[2]

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