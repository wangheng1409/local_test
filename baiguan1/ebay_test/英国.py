# !/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import requests
import time


url='https://www.ebay.co.uk/b/Travel-Backpacks-Rucksacks/16081/bn_9536129?_pgn=1'

headers={
'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'accept-encoding':'gzip, deflate, br',
'accept-language':'zh-CN,zh;q=0.9',
'cache-control':'max-age=0',
'upgrade-insecure-requests':'1',
'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
}

ret=requests.get(url,headers=headers,verify=False).text
print(ret)

