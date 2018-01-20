# !/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import requests
import time

shop_id=57939393
base_url='http://www.dianping.com/shop/{}'
url=base_url.format(str(shop_id))
print(url)

headers={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cache-Control':'max-age=0',
    'Cookie':'s_ViewType=10; _hc.v=29baff58-d6b8-e6bf-eb62-afe5601af173.1511407720; _lxsdk_cuid=15fe6eb96cbc-0cd140a2049be4-31657c00-384000-15fe6eb96cec8; _lxsdk=15fe6eb96cbc-0cd140a2049be4-31657c00-384000-15fe6eb96cec8; _lxsdk_s=15fe6eb96d3-9fa-a25-186%7C%7C18',
    'Host':'www.dianping.com',
    'Proxy-Connection':'keep-alive',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
}
#
ret=requests.get(url,headers=headers).text
print(ret)

