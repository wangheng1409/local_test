# !/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import requests
import time


url='http://wechat.funxdata.com/'
headers={
    'Host': 'wechat.funxdata.com',
    'Upgrade-Insecure-Requests': '1',
    'Accept-Encoding': 'gzip, deflate',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Cookie': 'ci_session=fe830a186d7da00ba104aa053ae92afb820efaa7',
    'Accept-Language': 'zh-cn',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.21 NetType/WIFI Language/zh_CN',
}

# ret=requests.get(url,headers=headers).text
# print(ret)


url1='http://wechat.funxdata.com/apartment/7'
url2='http://wechat.funxdata.com/roomtype/29'
ret=requests.get(url2,headers=headers).text
print(ret)

