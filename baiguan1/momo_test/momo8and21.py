# !/usr/bin/env python
# -*- coding:utf-8 -*-


import requests
import json
import random


def random_ssid():
    return ''.join(
        map(lambda i: chr(random.randint(97, 122)) if random.randint(1, 4) in [1, 2] else str(random.randint(0, 9)),
            range(32)))

def fortune_charm(stid):
    data1={
        'stid'	:str(stid),
        'src'	:'url',
    }

    url1='https://web.immomo.com/webmomo/api/scene/profile/infosv2'

    header1={
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 's_id='+random_ssid()+'; cId=54898950411749; Hm_lvt_c391e69b0f7798b6e990aecbd611a3d4=1498548990; Hm_lpvt_c391e69b0f7798b6e990aecbd611a3d4=1498549010',
        'Host': 'web.immomo.com',
        'Origin': 'https://web.immomo.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    ret=requests.post(url=url1,data=data1,verify=False,headers=header1).content.decode()
    ret_dic=json.loads(ret)
    ec=ret_dic.get('ec')
    if ec ==200:
        rd=ret_dic['data'].get('rid','')
        token=ret_dic['data'].get('token','')

        data2={
            'dmid':str(stid),
            'rd':str(rd),
            'token':token,
            'source':'profile',
        }
        url2='https://web.immomo.com/webmomo/api/scene/profile/userinfo'
        ret = requests.post(url=url2, data=data2, verify=False, headers=header1).content.decode()
        result=json.loads(ret)
        fortune=result['data'].get('fortune','')
        charm=result['data'].get('charm','')
        return fortune,charm


fortune,charm=fortune_charm(332348334)
print(fortune,charm)