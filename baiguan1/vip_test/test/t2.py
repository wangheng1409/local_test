import requests
import hashlib
import json


def md5(password):
    '''
    对密码进行加密
    :param pwd: 密码
    :return:
    '''
    hash = hashlib.md5()
    hash.update(bytes(password, encoding='utf-8'))
    return hash.hexdigest()


def requests_sessionid(phone,password):

    ur='https://live-api.immomo.com/v2/user/login_phone'
    data={
        'iosEditionName': 'iosEditionForNormal',
        'ios_uuid': '1C417545-BD01-4F43-BB4A-A118FF06498D',
        'lat': '39.94685910424272',
        'lng': '116.4133660299107',
        'molive_uid': '7515fa3fec545067493b3aa15b671111',
        'passwd': md5(password),
        'phone': str(phone),
        'uuid': '7515fa3fec545067493b3aa15b671111',
    }

    head={
        'Host': 'live-api.immomo.com',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Cookie': 'SESSIONID=9c7d6f65f58810435ef505696e9311aa',
        'User-Agent': 'Molive/1.9.1 ios/602 (iPhone 7; iOS 10.1.1; en_US; iPhone9,1; S1)',
        'Accept-Language': 'en-US;q=1, zh-Hans-US;q=0.9',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    w=requests.post(url=ur,headers=head,data=data,verify=False)
    try:
        return json.loads(w.text)['data']['sessionid']
    except KeyError:
        return json.loads(w.text)

if __name__ == "__main__":
    print(requests_sessionid(18518077377,'cdfcdf'))