# !/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json

url = 'https://hdgateway.zto.com/gateway.do'
header = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'hdgateway.zto.com',
    'Origin': 'http://www.zto.com',
    'Referer': 'http://www.zto.com/express/expressCheck.html',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'X-ZOP-NAME': 'WayBill_GetDetail',        }

data={
    'billCode':'719442916877'
}

ret=requests.post(url,headers=header,data=data).text
ret=json.loads(ret)
log_item=ret['result']['logisticsRecord']
item={}
item['oid'] = '719442916877'
item['source'] = 'zto'
item['status'] = 3
item['origin_province'] =log_item[-1][-1]['scanSite']['province']
item['origin_city'] =log_item[-1][-1]['scanSite']['city']
item['dest_province'] =log_item[0][0]['scanSite']['province']
item['dest_city'] =log_item[0][0]['scanSite']['city']
item['dt'] =log_item[-1][-1]['scanDate']
item['df'] =log_item[0][0]['scanDate']
item['raw'] = json.dumps(ret)

print(item)
