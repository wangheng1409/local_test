#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests


def auth(http_proxy, depcode='SZX', arrcode='TSN', sel_date='2016-12-23'):
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
    year, month, day = sel_date.split('-')
    url1 = 'http://bk.travelsky.com/bkair/reservation/flightQuery.do'
    headers1 = {
        'Host': ' bk.travelsky.com',
        'Connection': ' keep-alive',
        'Cache-Control': ' max-age=0',
        'Origin': ' http://bk.travelsky.com',
        'Upgrade-Insecure-Requests': ' 1',
        'User-Agent': ' Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': ' text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': ' http://bk.travelsky.com/bkair/index.jsp',
        'Accept-Encoding': ' gzip, deflate',
        'Accept-Language': ' zh-CN,zh;q=0.8'
    }

    cookie = None  # requests.utils.dict_from_cookiejar(session.cookies)
    return cookie, headers1, url1 + '?' + sel_date + depcode + arrcode


if __name__ == '__main__':
    auth()
