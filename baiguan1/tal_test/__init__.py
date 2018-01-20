# !/usr/bin/env python
# -*- coding:utf-8 -*-

# !/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import requests
import time


url='https://xesapi.speiyou.cn/v1/py/course/list'

headers={
    'Host': 'xesapi.speiyou.cn',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept-Language': 'zh-cn',
    'Accept': '*/*',
    'Connection': 'keep-alive',
    'User-Agent': '%E5%AD%A6%E8%80%8C%E6%80%9D/322 CFNetwork/811.5.4 Darwin/16.7.0',
}


#0 15 4028871d280025ea012800b206313809 3 8.00 1
data={
   'claCourseType':		0,
'cla_term_id':		5,
'client_type':		1,
'gradeId':		5,
'isHiddenFull'	:0	,
'lev_degree':	'1.00',
'limit'	:	99,
'page'	:	1,
'sign'	:	'A38066A940401B1682E3D2EC6765DD55',
'subjectIds'	:	'ff80808127d77caa0127d7e10f1c00c4',
'teaId'	:	'',
'timeType':		'',
'token':		'KC2uS7wPFv5bIn/LmvsgWrDPW/9fgXNNTyi5xBRzEPLs1/7s225FkSJTwnJ0EurSbJWn WuNlwfotnnHzW Cav7uHhuezYSn8pacDInbTFL/LSGnYuXTu8XCqmwCrsW4s2V/r0hJE2h8LSxYZpzZ9bojf5Gp9P0IM/7ybpPUi2w=',
'tutorTeaId':'',
'v'	:	'6.0.0',
'venueId':	''	,
'year':	'',

}

ret=requests.post(url,headers=headers,data=data,verify=False).text
ret=json.loads(ret)
room_list = ret['data']['queryData']
print(ret['data'],len(room_list))





