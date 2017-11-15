# !/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import requests
import time


url='https://sz.inboyu.com/project/list/?r=project%2Flist'

headers={
    'Host': 'sz.inboyu.com',
    'Accept-Encoding': 'gzip, deflate',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Cookie': 'PHPSESSID=aj98k03p3o87heg82ms1eva1t1; acw_tc=AQAAAGYEJH+r7wQAKoRFeTK2yz+2qRSt',
    'Connection': 'keep-alive',
    'Accept-Language': 'zh-cn',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.21 NetType/WIFI Language/zh_CN',
}

ret=requests.get(url,headers=headers).text
print(ret)


# url2='https://sz.inboyu.com/room-type/list?project_id=39dd9615-44c4-5d5e-9ace-b7cf3ebd354e'
#
# ret=requests.get(url2,headers=headers).text
# print(ret)

url3='https://sz.inboyu.com/room-type/detail?id=39dd9784-ed23-8fac-ea45-36c22aed54e2'
