# !/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import requests
import time


url='https://xesapi.speiyou.cn/v1/py/class/courseInfo'

headers={
    'Host': 'xesapi.speiyou.cn',
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Tingyun-Id': 'zAj7Vu-0QAI;c=2;r=1538626067',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-cn',
    'Accept': '*/*',
    'Connection': 'keep-alive',
    'User-Agent': '%E5%AD%A6%E8%80%8C%E6%80%9D/322 CFNetwork/811.5.4 Darwin/16.7.0',
}

data={
    'client_type': 1,
    'id': 'ff808081601101440160119f65c015e8',
    'isCoordinate': 1,
    'isSatisfied': 1,
    'isShowStudent': 1,
    'isShowTeacher': 1,
    'sign': '85CF190BB4B87E8B51C293693DA7A826',
    'token': 'KC2uS7wPFv5bIn/LmvsgWrDPW/9fgXNNTyi5xBRzEPLs1/7s225FkSJTwnJ0EurSbJWn WuNlwfotnnHzW Cav7uHhuezYSn8pacDInbTFL/LSGnYuXTu8XCqmwCrsW4s2V/r0hJE2h8LSxYZpzZ9bojf5Gp9P0IM/7ybpPUi2w=',
    'v': '6.0.0',
}

ret=requests.post(url,headers=headers,data=data,verify=False).text
ret=json.loads(ret)

print(ret)





