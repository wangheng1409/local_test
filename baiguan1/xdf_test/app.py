# !/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import datetime
import json
t=str(datetime.datetime.now().strftime( '%Y-%m-%d %H:%M:%S' ))
today=str(datetime.date.today())

url_token='http://api1.xdf.cn/SoukeRest/oauth/token'

headers_token={
    'Host': 'api1.xdf.cn',
    'Authorization': 'Basic NTAwMTp2NWFwcGtleV9tb2JfeXNuJHhheg==',
    'Accept': '*/*',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'User-Agent': 'xdfapp/3.1.4 (iPhone; iOS 10.3.3; Scale/2.00)',
}

data={
   'client_id':'5001',
   'client_secret':'v5appkey_mob_ysn$xaz',
   'grant_type':'client_credentials',
}

ret=requests.post(url_token,headers=headers_token,data=data).text
ret=json.loads(ret)
access_token=ret['access_token']

print(access_token)
url='http://api1.xdf.cn/SoukeRest/Class/GetClassBySearch?' \
    'access_token='+access_token+'&' \
    'applyState=1&' \
    'cityId=1&' \
    'date='+today+'&' \
    'hide=1&' \
    'keyword=GMEC181130&' \
    'pageIndex=1&' \
    'pageSize=15&' \
    'timestamp='+t

headers={
'Host'	:'api1.xdf.cn',
'Accept-Encoding':	'gzip, deflate',
'Accept'	:'*/*',
'Accept-Language':	'zh-Hans-CN;q=1, en-CN;q=0.9',
'Connection'	:'keep-alive',
'User-Agent'	:'xdfapp/3.1.4 (iPhone; iOS 10.3.3; Scale/2.00)',
}

ret=requests.get(url,headers=headers).text
print(ret)
