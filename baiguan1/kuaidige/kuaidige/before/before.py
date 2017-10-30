import requests
import json
import time
import random

USER_AGENTS = [
    "android/4.4.4 (Xiaomi;MI 4LTE) letvVideo/5930/aps_cm_00_3.0.7.0",
    "Mozilla/5.0 (Android; U; zh-CN) AppleWebKit/533.19.4 (KHTML, like Gecko) AdobeAIR/16.0",
    "LetvIpadClient/5.9.3 (iPad; iOS 7.1; Scale/2.00)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13D15 Safari/601.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D201 Safari/9537.53",
    "inke/2.6.1 (iPhone; iOS 9.2.1; Scale/2.00)",
    "Dalvik/1.6.0 (Linux; U; Android 4.4.4; SM-W2015 Build/KTU84P)",
    "Redmi 3; MIUI/V7.1.3.0.LHPCNCK",
    "Mozilla/5.0 (iPad; CPU OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13D15 Safari/601.1",
    "MomoChat/6.6 Android/645 (SCH-W2013; Android 4.0.4; Gapps 0; zh_CN; 13)",
    "Dalvik/2.1.0 (Linux; U; Android 5.1; MX4 Build/LMY47I)",
    "Dalvik/2.1.0 (Linux; U; Android 5.0; SM-N9008S Build/LRX21V)",
    "Dalvik/1.6.0 (Linux; U; Android 4.4.2; 2014501 MIUI/KHHCNBF5.0)",
    "Dalvik/1.6.0 (Linux; U; Android 4.2.2; U819 Build/ZTEU819)",
    "MI 3; MIUI/V7.2.1.0.KXCCNDA",
    "Dalvik/2.1.0 (Linux; U; Android 5.1; MX4 Build/LMY47I)",
    "Dalvik/2.1.0 (Linux; U; Android 5.0; SM-N9008S Build/LRX21V)",
]

def headers(latitude,longitude):


    s = {"latitude": latitude+str(random.randrange(100,999)),
         "longitude": longitude+str(random.randrange(100,999)),
         # "latitude": "39.951599",
         # "longitude": "117.420467",
         "ltype": "mars",
         "appid": "com.Kingdee.Express",
         "versionCode": 439,
         "os_version": "android5.0.2",
         "os_name": "",
         "t": int(str(time.time()).split('.')[0]),
         "tra": "3a432dc8-a32a-4241-a0bb-56ddfab191d3",
         "uchannel": "null",
         "nt": "wifi",
         "mType": "mars",
         "mLatitude": float('39.'+str(random.randrange(100000,999999))),
         "mLongitude": float('117.'+str(random.randrange(100000,999999))),
         "adcode": "",
         "address": ""}

    data = {
        'method': 'courieraround',
        'hash': '1C1F6A149DB30FE350F635C72FB6561D',
        'userid': '0',
        'json': json.dumps(s),
    }

    url = 'http://j.kuaidi100.com/searchapi.do'

    header = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': random.choice(USER_AGENTS),
        'Host': 'j.kuaidi100.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
    }
    return  url,header,data

#
if __name__ == '__main__':
    #start：
        # "latitude": "39.260",      "latitude": "41.030",
        # "longitude": "115.250",    "longitude": "117.300",
    url,headers,data = headers("39.951","117.420")
    print(requests.post(url=url,data=data,verify=False,headers=headers).text)