# !/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import random
import time
import json
from lichao_test import pytesseract
from PIL import Image

session=requests.session()
header={
'Host':	'ykjcx.yundasys.com',
'Cache-Control':	'max-age=0',
'Origin':	'http://www.yundaex.com',
'Upgrade-Insecure-Requests'	:'1',
'Content-Type'	:'application/x-www-form-urlencoded',
'User-Agent':	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
'Accept':	'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Referer'	:'http://www.yundaex.com/cn/index.php',
'Accept-Encoding':	'gzip, deflate',
'Accept-Language':	'zh-CN,zh;q=0.8',
'Cookie'	:'PHPSESSID=trvsjif5mdrs44qjmsrch39fq7; JSESSIONID=1bNyZLCSYLNG7gNmMYNb9gGfp3QNt8LdFJWDJ7hJPj0v2QTf3v7J!495833763',
}
data={
    'wen':'3959581169085'
}
ret=session.post('http://ykjcx.yundasys.com/go.php?wen=3959581169085',data=data,headers=header,verify=False).text
# print(ret)

header_amage={
    'Host'	:'ykjcx.yundasys.com',
    'User-Agent':	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
    'Accept'	:'image/webp,image/apng,image/*,*/*;q=0.8',
    'Referer':	'http://ykjcx.yundasys.com/go.php',
    'Accept-Encoding':	'gzip, deflate',
    'Accept-Language':	'zh-CN,zh;q=0.8',
    'Cookie'	:'JSESSIONID=1phdZLJJ3FFlPFwWs1J62tpBB8QRQTR0kBRhr9vTvySRv4J1FyQ1!495833763; PHPSESSID=trvsjif5mdrs44qjmsrch39fq7',
}
f=open('b.png','wb')
f.write(session.get('http://ykjcx.yundasys.com/zb1qBpg2.php',headers=header_amage,verify=False).content)
f.close()
pil_im=Image.open('b.png').convert('L')
# pil_im.show()
time.sleep(2)
def initTable(threshold=200):
     table = []
     for i in range(256):
         if i > threshold:
             table.append(0)
         else:
             table.append(1)
     return table
binaryImage = pil_im.point(initTable(), '1')
binaryImage.show()
vcode = pytesseract.image_to_string(binaryImage)
print (vcode)
if not vcode:
    print('no')
else:

    result=eval(vcode.strip('='))
    print(result)

    header_r={
        'User-Agent':	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',
        'Accept-Encoding'	:'gzip, deflate',
        'Accept'	:'image/webp,image/apng,image/*,*/*;q=0.8',
        'Connection':	'keep-alive',
        'Host'	:'ykjcx.yundasys.com',
        'Referer'	:'http://ykjcx.yundasys.com/go.php',
        'Accept-Language':	'zh-CN,zh;q=0.8',
        'Cookie':	'JSESSIONID=1phdZLJJ3FFlPFwWs1J62tpBB8QRQTR0kBRhr9vTvySRv4J1FyQ1!495833763; PHPSESSID=trvsjif5mdrs44qjmsrch39fq7',
    }
    data={
        'wen'	:'3959581169085',
        'debug'	:'1',
        'lang':	'C',
        'hh':	'23',
        'yzm':	str(result),
    }
    ret1=session.post('http://ykjcx.yundasys.com/go_wsd.php',data=data,headers=header_r,verify=False).text

    print(ret1)
#
#
