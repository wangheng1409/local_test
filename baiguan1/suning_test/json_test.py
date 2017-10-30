# !/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import requests
s=requests.get('https://search.suning.com/emall/mobile/wap/clientSearch.jsonp?cityId=028&keyword=&channel=&cp=0&ps=120&st=8&set=5&cf=0&iv=-1&ci=157252&ct=-1&channelId=WAP&sp=&sg=&sc=&prune=&operate=0&isAnalysised=0&istongma=1&v=99999999&callback=success_jsonpCallback').text
left = s.index('{')
tmp=s[left:].strip()[:-2]
s=json.loads(s)
print(s)