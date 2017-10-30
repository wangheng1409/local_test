import requests
import json
import time
data={
    'longitude': 116.4188028016724,
    'latitude': 39.95323850544272,
    'errMsg': 'getMapCenterLocation:ok',
    'citycode': '010',
    'wxcode': '011IPLrb22LoeQ0O2gsb2avxrb2IPLr7',
}

url='https://mwx.mobike.com/mobike-api/rent/nearbyBikesInfo.do'

headers={
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_0_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13A452 MicroMessenger/6.5.7 NetType/WIFI Language/zh_CN',
    'accept-language': 'zh-cn',
    # 'time': 1498123885594,
    'time': str(time.time()).split('.')[0],
    'open_src': 'list',
    'referer': 'https://servicewechat.com/wx80f809371ae33eda/48/page-frame.html',
    'content-type': 'application/x-www-form-urlencoded',
    'platform': '3',
    'citycode': '010',
    'lang': 'zh',
    'eption': 'e1bc2',
    'wxcode': '011IPLrb22LoeQ0O2gsb2avxrb2IPLr7',
    'content-length': '140',
    'accept-encoding': 'gzip, deflate',
}

for k,v in headers.items():
    print(k,':',v)
ret=requests.post(url=url,data=data,headers=headers,verify=False).text
print(ret)