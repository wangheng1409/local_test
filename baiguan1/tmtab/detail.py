# !/usr/bin/env python
# -*- coding:utf-8 -*-

import requests

url='https://detailskip.taobao.com/service/getData/1/p1/item/detail/sib.htm?itemId=554781097315&sellerId=751796500&modules=dynStock,qrcode,viewer,price,duty,xmpPromotion,delivery,upp,activity,fqg,zjys,couponActivity,soldQuantity,originalPrice,tradeContract&callback=onSibRequestSuccess'
# url='https://detail.m.tmall.com/item.htm?id=545641241138&scm=1007.14688.88974.0&pvid=f4b0e9cb-cc6a-4df1-bf1d-94b449b15803&spm=a223j.8443192.recommend.3'
headers={
        'accept':'*/*',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'zh-CN,zh;q=0.8',
        'cookie':'v=0; cookie2=1c7ae7be4a6fd210cd099bc6285e8d5c; t=d043ac5542cce176c9a040761684b15d; thw=cn; _m_h5_tk=36ef9bb8cb2b34d9e7ad28da509074d0_1505457872316; _m_h5_tk_enc=0ee46eb3096ada312ce7e747cac6320a; miid=1996970617266021810; isg=AhAQzygxfSisGCEEVEhMqpER4ViicedKGbckeArgemouRbTvsujcso-3azte; cna=7UIUEr29+A0CAXaQhSXRK9Rc; _tb_token_=f3333657e7e33; mt=ci%3D-1_0; uc1=cookie14=UoTcCi87CtVaEg%3D%3D',
        'referer':'https://item.taobao.com/item.htm?spm=5148.10035500.848425.34.63348a62RWv21x&id=554781097315',
        'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
        }
from bo_lib.general import ProxyManager
pm = ProxyManager()
print(pm.getProxyV2())
# ret=requests.get(url, headers=headers, proxies=pm.getProxyV2(), timeout=10)
ret=requests.get(url, headers=headers, proxies=pm.getProxyV2(), timeout=10)
# ret=requests.get(url, headers=headers, timeout=10,verify=False)
print(ret.status_code)
print(ret.url)
print(ret.text)