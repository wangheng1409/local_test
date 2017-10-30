
import pymongo
from collections import defaultdict


uri = 'mongodb://root:Baiguan2016@60.205.152.167:3717'
mongo = pymongo.MongoClient(uri)
db1 = mongo['xdf']['courses']
col = db1.find({'ts_str':'2017-06-16'}, no_cursor_timeout=True)

column={}
begin_time={}

c=0
for item in col:
    if c % 10 == 0:
        print('store_id_num', c)
    c += 1
    if item['city'] not in column:
        column[item['city']]={}
    if item['column'] not in column[item['city']]:
        column[item['city']][item['column']]=0
    column[item['city']][item['column']]+=1
    if item['city'] not in begin_time:
        begin_time[item['city']] = {}
    if item['begin_time'] not in begin_time[item['city']]:
        begin_time[item['city']][item['begin_time']] = 0

    begin_time[item['city']][item['begin_time']]+=1

print(column,'\n')
print(begin_time,'\n')
