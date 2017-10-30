#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
def ns_authentication(http_proxy,depcode='SJW', arrcode='BAV',sel_date='2016-12-22'):
    '''
    :param depcode: 起始三字码
    :param arrcode: 到达三字码
    :param sel_date: 出发日期
    :return: cookie, header, url
    '''
    session = requests.session()
    session.proxies = {
        "http": http_proxy,
    }
    url1 = 'http://www.hbhk.com.cn/airTicketBook/flightOption/index.shtml'
    headers1 = {
        'Host':' www.hbhk.com.cn',
        'Connection':' keep-alive',
        'Upgrade-Insecure-Requests':' 1',
        'User-Agent':' Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36',
        'Accept':' text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer':' http://www.hbhk.com.cn/',
        'Accept-Encoding':' gzip, deflate, sdch',
        'Accept-Language':' zh-CN,zh;q=0.8'
    }
    data = {
        'dept': depcode,
        'arri': arrcode,
        '_date': sel_date
    }
    ret1 = session.get(url1, headers=headers1,params=data)
    url2='http://www.hbhk.com.cn/webapi/flight'
    headers2={
        'Host': ' www.hbhk.com.cn',
        'Connection': ' keep-alive',
        'Accept': ' application/json, text/plain, */*',
        'User-Agent': ' Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36',
        'Referer': url1+'?'+'&dept='+depcode+'&arri='+arrcode+'&_date='+sel_date,
        'Accept-Encoding': ' gzip, deflate, sdch',
        'Accept-Language': ' zh-CN,zh;q=0.8'
    }
    cookie = requests.utils.dict_from_cookiejar(session.cookies)
    return cookie, headers2, url2

if __name__ == '__main__':
    ns_authentication()
