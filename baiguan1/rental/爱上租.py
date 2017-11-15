# !/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import requests
import time


url='http://m.ishangzu.com/hz/zufang/p3/?_='+str(time.time()).replace('.','')[:-3]

headers={
    'Host'	:'m.ishangzu.com',
    # 'Cookie'	:'Hm_lpvt_322b01787e83a3202d487d2e3dcc9152=1509594165; Hm_lvt_322b01787e83a3202d487d2e3dcc9152=1509594126,1509594157; Hm_lpvt_2d1fb77e9aeb419bd6ce2ed0ad9592af=1509594165; Hm_lvt_2d1fb77e9aeb419bd6ce2ed0ad9592af=1509594126,1509594156; XSRF-TOKEN=eyJpdiI6ImlWUFY3V0JkVE1ubDBZMTFQNFk1N2c9PSIsInZhbHVlIjoiMTRHY1wvb3lrenV1Z1QxSHE0VVE1Z3pKWWUzMmNNRDVKK3FaR2NMRURkWUt4WGZpbzlLOFBLdmtIRFQ3clBsWDBKanFKQWxieUNIbG1aNG4yVGVuV1JBPT0iLCJtYWMiOiI3NTJkN2E3YTEyN2Q1OTc0NGJhZWJlYTFjY2M4MjZiZWMzZmU0MWM0YzhmYzcxNjQ5MmRjNDlkYTg4ZWYxY2YxIn0%3D; isz_session=eyJpdiI6IjF3QzZobVc1S1JNWml4NTkxclFQN0E9PSIsInZhbHVlIjoiTml5a1VONk1sK3Z4OHhUSjkxZkVCMXpKa2tGOVwvSWtqczk4THl4TXdZTGlNWUNLem5idzVqZ01ydmNVSCtONzgxbDByNEJwbDV2QzcwSFhGVHlsOGx3PT0iLCJtYWMiOiI3ODE1ZmVmMzExODRlZGJjMjA2M2QxOWM3ZWYyNGU4ZDRmZGUyMDhkN2JjMzUyOThiNDk0MTMwYzA0YTc3NzRmIn0%3D; isz_uid=5821c82a-9006-4902-a76e-f788a8793e8e',
    'Accept'	:'text/html',
    'User-Agent'	:'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X; zh-CN) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/14G60 UCBrowser/11.6.7.1025 Mobile  AliApp(TUnionSDK/0.1.20)',
    'X-Requested-With'	:'XMLHttpRequest',
    'Accept-Language':	'zh-cn',
    'Referer':	'http://m.ishangzu.com/hz/zufang/',
    'Accept-Encoding'	:'gzip, deflate',
}

ret=requests.get(url,headers=headers).text
print(ret)

