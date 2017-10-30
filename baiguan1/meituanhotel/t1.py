import requests
import random

def headers(offset,cityId,lat,lng,endDay,startDay):
    url1='https://ihotel.meituan.com/hbsearch/HotelSearch?' \
        'newcate=1' \
        '&cateId=20' \
        '&uuid=1A6E888B4A4B29B16FBA1299108DBE9C287336CBAB3B2221A984590EDC9271CA' \
        '&attr_28=129' \
        '&limit=20&offset=0&cityId=1&mypos=39.95%2C116.4145&sort=defaults' \
        '&endDay=20170614&startDay=20170614' \
        '&sourceType=hotel' \
        '&client=iphone' \
        '&utm_medium=WEIXINPROGRAM&utm_term=8.2.0&version_name=8.2.0&utm_campaign=entry%253DMTHotel'
    url2='https://ihotel.meituan.com/hbsearch/HotelSearch?newcate=1' \
         '&cateId=20&uuid=2A6E888B2A4B29B26FBA1299108DBE9C287336CZAB3B2221A984590EDZ2272CA' \
         '&attr_28=129&limit=20&offset=0&cityId=1&mypos=39.95%2C116.4145&sort=defaults&endDay=20170614&startDay=20170614' \
         '&distance=10000&sourceType=hotel' \
         '&client=iphone&utm_medium=WEIXINPROGRAM&utm_term=8.2.0&version_name=8.2.0&utm_campaign=entry%253DMTHotel'
    url='https://ihotel.meituan.com/hbsearch/HotelSearch?' \
        'newcate=1' \
        '&cateId=20' \
        '&uuid=1A6E888B4A4B29B16FBA1299108DBE9C287336CBAB3B2221A984590EDC9271CA' \
        '&attr_28=129' \
        '&limit=20&offset='+str(offset)+'&cityId='+str(cityId)+'&mypos='+str(lat)+'%2C'+str(lng)+'&sort=defaults' \
        '&endDay='+str(endDay)+'&startDay='+str(startDay)+'' \
        '&sourceType=hotel' \
        '&client=iphone' \
        '&utm_medium=WEIXINPROGRAM&utm_term=8.2.0&version_name=8.2.0&utm_campaign=entry%253DMTHotel'
    momo_headers = {
        'Host':	'ihotel.meituan.com',
        'Referer':	'https://servicewechat.com/wx7649daed8f2335c4/4/page-frame.html',
        'Accept-Encoding':	'gzip, deflate',
        'Content-Type':	'application/json',
        'Accept-Language':	'zh-cn',
        'Accept':	'*/*',
        'Connection':	'keep-alive',
        'User-Agent':	'Mozilla/5.0 (iPhone; CPU iPhone OS 9_0_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13A452 MicroMessenger/6.5.7 NetType/WIFI Language/zh_CN'
    }
    return  url2,momo_headers

#
if __name__ == '__main__':

    url,headers = headers(0,1,39.95,116.4145,20170614,20170614)
    print(requests.get(url, headers=headers,verify=False).text)