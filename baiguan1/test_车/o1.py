


import requests
import json


data={
    'token'	:'307345E0-32C0-11E7-9270-234CDE175C92',
    'source'	:0,
    'source-version':	9999,
    'lat'	:39.951834,
    'lng':	116.417403,
}

url='https://san.ofo.so/ofo/Api/nearbyofoCar'

header={
    'Host':	'san.ofo.so',
    'Referer':	'https://common.ofo.so/newdist/?utm_source=download&utm_medium=smwappz&',
    'Accept':	'*/*',
    # 'Content-Type':	'multipart/form-data; boundary=----ofo-boundary-MC42MzU4MTY3',
    'Accept-Language':	'zh-cn',
    'Accept-Encoding':	'gzip, deflate',
    'Origin':	'https://common.ofo.so',
    'Content-Length':	'516',
    'Connection' :'keep-alive',
    'User-Agent':	'Mozilla/5.0 (iPhone; CPU iPhone OS 9_0_2 like Mac OS X; zh-CN) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/13A452 UCBrowser/10.7.0.643 Mobile'
}

ret=requests.post(url=url,data=data,verify=False,headers=header)
print(ret.text)