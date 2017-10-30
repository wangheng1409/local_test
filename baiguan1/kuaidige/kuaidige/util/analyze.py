import datetime
import pymongo
from collections import defaultdict
today=str(datetime.datetime.today())

uri = 'mongodb://root:Baiguan2016@60.205.152.167:3717'
mongo = pymongo.MongoClient(uri)
db1 = mongo['kuaidige']['kuaidige_detail']
col = db1.find({'ts_string':{'$lt':'2017-06-28'},'cityName':'上海'}, no_cursor_timeout=True)

# s=defaultdict(set)
# c=0
# for item in col:
#     if c % 1000 == 0:
#         print('store_id_num', c)
#     c += 1
#
#     s[item['companyName']].add(item['courierName']+'|'+item['courierTel'])
#
# for a,b in sorted(s.items(),key=lambda x:len(x[1]),reverse=True):
#   print(a,len(b))

t=defaultdict(set)
c=0
for item in col:
    if c % 1000 == 0:
        print('store_id_num', c)
    c += 1
    try:
        t[item['cityName']].add(item['courierName']+'|'+item['courierTel'])
    except:
        print(item)

# for a,b in sorted(t.items(),key=lambda x:len(x[1]),reverse=True):
#   print(a,len(b))
#
# print(t)
s1=t['上海']
print(s1)
col1 = db1.find({'ts_string':{'$lt':'2017-06-28'},'cityName':'上海'}, no_cursor_timeout=True)

tt=defaultdict(set)
c=0
for item in col:
    if c % 1000 == 0:
        print('store_id_num', c)
    c += 1
    try:
        tt[item['cityName']].add(item['courierName']+'|'+item['courierTel'])
    except:
        print(item)
s2=tt['上海']

print(s2-s1)