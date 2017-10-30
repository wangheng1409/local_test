# !/usr/bin/env python
# -*- coding:utf-8 -*-

import requests

headers={
    'Host'	:'www.yundaex.com',
    'Accept':	'application/json, text/javascript, */*; q=0.01',
    'Origin':	'http://www.yundaex.com',
    'X-Requested-With':	'XMLHttpRequest',
    'User-Agent'	:'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
    'Content-Type':	'application/x-www-form-urlencoded; charset=UTF-8',
    'Referer':	'http://www.yundaex.com/cn/index.php',
    'Accept-Encoding':	'gzip, deflate',
    'Accept-Language':	'zh-CN,zh;q=0.8',
    'Cookie'	:'PHPSESSID=gojjp93t1k8i2bb66fh4io0p16; Hm_lvt_e5bfe632ac0deb9484186e22dfa45545=1506312752; Hm_lpvt_e5bfe632ac0deb9484186e22dfa45545=1506312752',
}
data={
'waybill':	'3959581169085',
'type':	'now',
}

ret=requests.post('http://www.yundaex.com/cn/data/waybill_search.php',headers=headers,data=data,verify=False).text
print(ret)