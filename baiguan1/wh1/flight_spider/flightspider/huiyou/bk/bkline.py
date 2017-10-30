#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import json
import datetime
from flightspider import database


line_list=['SYX-TSN','SYX-NGB','SYX-ZUH','SYX-CSX','URC-SIA','BHY-KHN','NKG-KMG','NNG-SZX',
'NNG-SIA','NNG-CKG','KHN-BHY','KHN-TSN','NTG-TSN','NTG-HAK','XMN-CSX','HFE-KMG',
'HRB-TSN','TSN-SYX','TSN-KHN','TSN-NTG','TSN-HRB','TSN-NGB','TSN-CAN','TSN-CTU',
'TSN-KWL','TSN-HAK','TSN-SZX','TSN-ZUH','TSN-SIA','TSN-CKG','TSN-CSX','NGB-SYX',
'NGB-TSN','CAN-TSN','HUZ-CSX','CTU-TSN','CTU-CSX','KMG-NKG','KMG-HFE','KMG-JHG',
'KMG-CSX','HGH-SHE','HGH-CSX','KWL-TSN','WUS-SZX','SHE-HGH','SHE-TAO','HAK-NTG',
'HAK-TSN','HAK-SZX','SZX-NNG','SZX-TSN','SZX-WUS','SZX-HAK','SZX-AEB','ZHA-CSX',
'ZUH-SYX','ZUH-TSN','AEB-SZX','JHG-KMG','SIA-URC','SIA-NNG','SIA-TSN','SIA-CSX',
'CKG-NNG','CKG-TSN','CKG-CSX','CSX-SYX','CSX-XMN','CSX-TSN','CSX-HUZ','CSX-CTU',
'CSX-KMG','CSX-HGH','CSX-ZHA','CSX-SIA','CSX-CKG','CSX-TAO','TAO-SHE','TAO-CSX']
l=[]

for line in line_list:
    depCode, arrCode=line.split('-')
    l.append([line,depCode,arrCode])
now=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# for item in l:
#     sql="insert into spider_policy (company, name, depCode, arrCode, dateRange, spiderName,spiderCycle, worker,state,priority,weeks,createtime) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
#     database.db.insert(sql,'BK',item[0],item[1],item[2],
#                        60, 'bkdetail', 15, '0001',1,1,'1,2,3,4,5,6,7',now)