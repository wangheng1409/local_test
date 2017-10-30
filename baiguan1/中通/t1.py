import requests
import json
import time



s={"latitude":"39.951599",
   "longitude":"117.420467",
   "ltype":"mars",
   "appid":"com.Kingdee.Express",
   "versionCode":439,
   "os_version":"android5.0.2",
   "os_name":"Redmi Note 3",
   "t":1498189859537,
   "tra":"3a432dc8-a32a-4241-a0bb-56ddfab191d3",
   "uchannel":"null",
   "nt":"wifi",
   "mType":"mars",
   "mLatitude":39.961599,
   "mLongitude":117.420467,
   "adcode":"110101",
   "address":"北京市东城区和平里西街靠近雍和空间"}

data={
    'method'	:'courieraround',
    'hash'	:'1C1F6A149DB30FE350F635C72FB6561D',
    'userid':	0,
    'json'	:json.dumps(s),
}

url='http://j.kuaidi100.com/searchapi.do'

header={
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.0.2; Redmi Note 3 MIUI/V8.2.1.0.LHNCNDL)',
    'Host': 'j.kuaidi100.com',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'Content-Length': '824',
}

ret=requests.post(url=url,data=data,verify=False,headers=header)
print(ret.text)
# for k in json.loads(ret.text)['values']['info']['cars']:
#     print(k,)
print(time.time())