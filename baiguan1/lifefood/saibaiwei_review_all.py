# !/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import requests
import time

shop_id=2363917
page=1
base_url='http://www.dianping.com/shop/{}/review_all?pageno={}'
url=base_url.format(str(shop_id),str(page))
print(url)

headers={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cache-Control':'max-age=0',
    'Cookie':'_lxsdk_cuid=15fe1c3d145c8-0c44a572863426-31657c00-384000-15fe1c3d146c8; _lxsdk=15fe1c3d145c8-0c44a572863426-31657c00-384000-15fe1c3d146c8; _hc.v=d3998662-9c7f-58e2-f9b4-67857e7fc72e.1511321228; _lxsdk_s=15fe1c3d14c-a51-b9a-de%7C%7C14',
    'Host':'www.dianping.com',
    'Proxy-Connection':'keep-alive',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
}
#
ret=requests.get(url,headers=headers).text
print(ret)

