# !/usr/bin/env python
# -*- coding:utf-8 -*-
# !/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import requests
import time


url='https://mp.weixin.qq.com/wxagame/wxagame_bottlereport'

headers={
    'Host': 'mp.weixin.qq.com',
    'Referer': 'https://servicewechat.com/wx7c8d593b2c3a7703/7/page-frame.html',
    'Content-Type': 'application/json',
    'Accept': '*/*',
    'Accept-Language': 'zh-cn',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.6.1 NetType/WIFI Language/zh_CN',
}
s=int(str(time.time()).replace('.','')[:10])
s1=s+89
data={
	"base_req": {
		"session_id": "ayyjPDtrN+wGrTZgIJ/9VSQX5eRs9DGzFLMLoJlRcsOUkwy/ujZpCMRR0P0GMzP0nC3fBRlnRnaUAKpMfuh4+NV8VnSPuYkqTZ7KWk/F5tE9BqvmDpA7XdFTFZosVTbodsvzu4Ql2ewlaJOrIhFYgA==",
		"fast": 1,
		"client_info": {
			"platform": "ios",
			"model": "iPhone 5c (GSM)<iPhone5,3>",
			"system": "iOS 10.3.3"
		}
	},
	"report_list": [{
		"ts": s,
		"type": 10
	}, {
		"ts": s1,
		"type": 2,
		"score": 998,
		"best_score": 9,
		"break_record": 1,
		"duration": 560,
		"times": 34
	}]
}
ret=requests.post(url,headers=headers,data=json.dumps(data),verify=False).text
ret=json.loads(ret)

print(ret)





