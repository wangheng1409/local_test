# !/usr/bin/env python
# -*- coding:utf-8 -*-
import requests

print(requests.get('http://jandan.net/ooxx/page-399#comments',headers={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.9',
'Cache-Control':'max-age=0',
'Cookie':'_ga=GA1.2.1845607376.1512109278; _gid=GA1.2.257292887.1512109278; _gat_gtag_UA_462921_3=1',
'Host':'jandan.net',
'Proxy-Connection':'keep-alive',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
}).text)