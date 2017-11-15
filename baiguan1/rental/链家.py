# !/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import requests
import time


url='https://bj.lianjia.com/zufang/pg98/'

headers={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Cookie': 'lianjia_ssid=05b77fa7-2d20-42c7-a5d0-15bd5811a141',
    'Host': 'bj.lianjia.com',
    'Referer': 'https://bj.lianjia.com/zufang/pg1/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
}

ret=requests.get(url,headers=headers).text
print(ret)

