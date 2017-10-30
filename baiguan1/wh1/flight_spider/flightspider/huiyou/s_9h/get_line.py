#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import json
import datetime
from flightspider import database
r = requests.get('http://www.airchangan.com/zh/js/selectCityDatas.js')
r=r.text.encode('utf-8')
r= r[18:][:-1]

r=json.loads(r)['cityDatadefualt']
linkCity=r['linkCity']
citys=r['citys']
def get_cityname(code):
    for k,v in citys.items():
        if v==code:
            return k
l=[]

for k,v in linkCity.items():
    for city in v:
        name=get_cityname(k)+'-'+get_cityname(city)
        l.append([name,k,city])
print l
now=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
for item in l:
    sql="insert into spider_policy (company, name, depCode, arrCode, dateRange, spiderName,spiderCycle, worker,state,priority,weeks,createtime) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    database.db.insert(sql,'9H',item[0],item[1],item[2],
                       60, 's_9hdetail', 15, '0001',1,1,'1,2,3,4,5,6,7',now)