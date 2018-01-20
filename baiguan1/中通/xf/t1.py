
# !/usr/bin/env python
# -*- coding:utf-8 -*-

import requests

ret=requests.get(
    'http://www.sf-express.com/sf-service-owf-api/service/bills/221068242424/routes?app=bill&ticket=Q1Xeg1Su2QRlxMIzWOU8AiU7sgJ6a5_XFHbYzwdBlWpkjQKtT8ab7-ZaKKqZrxfD&lang=sc&region=cn&translate=',
    headers={
        'Host': 'www.sf-express.com',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Referer': 'http://www.sf-express.com/cn/sc/dynamic_function/waybill/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cookie': 'route=5278aef0da7cd3f27fdc3bca0ac79f75; Hm_lvt_32464c62d48217432782c817b1ae58ce=1505900310; Hm_lpvt_32464c62d48217432782c817b1ae58ce=1505900764; access-type=0; access-ip=27.204.117.183, 112.240.60.31, 10.117.228.201; ESG_OWF_NGINX_CNSZ17=ESG_OWF_CNSZ17_NGINX_WEB_226_133',
    },
)
s=ret.text

print(s)