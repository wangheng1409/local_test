import datetime
import pymongo
from collections import defaultdict
today=str(datetime.datetime.today())

uri = 'mongodb://root:Baiguan2016@60.205.152.167:3717'
mongo = pymongo.MongoClient(uri)
db1 = mongo['kuaidige']['kuaidige_detail']
col = db1.find({'ts_string':'2017-06-26'}, no_cursor_timeout=True)

s=defaultdict(set)
c=0
for item in col:
    if c % 1000 == 0:
        print('store_id_num', c)
    c += 1
    
    s[item['companyName']].add(item['courierName']+'|'+item['courierTel'])

for a,b in sorted(s.items(),key=lambda x:len(x[1]),reverse=True):
  print(a,len(b))