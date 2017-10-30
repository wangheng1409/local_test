#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests


def auth(depcode='XIY', arrcode='XNN', sel_date='2017-01-03'):
    '''
    :param depcode: 起始三字码
    :param arrcode: 到达三字码
    :param sel_date: 出发日期
    :return: cookie, header, url
    '''
    headers1 = {
        'Host': 'www.airchangan.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': ' Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'http://www.airchangan.com/zh/index.jsp',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    session = requests.session()
    year, month, day = sel_date.split('-')

    url1 = 'http://www.airchangan.com/InternetBooking/AirLowFareSearchExternal.do'
    data = {
        'searchType': 'FARE',
        'directFlightsOnly': 'false',
        'fareOptions': '1.FAR.X',
        'outboundOption.departureTime': 'NA',
        'lang': 'zh_CN',
        'tripType': 'OW',
        'flexibleSearch': 'false',
        'outboundOption.departureDay': day,
        'outboundOption.departureMonth': month,
        'outboundOption.departureYear': year,
        'guestTypes%5B0%5D.type': 'ADT',
        'guestTypes%5B1%5D.type': 'CNN',
        'guestTypes%5B2%5D.type': 'INF',
        'outboundOption.originLocationCode': depcode,
        'outboundOption.destinationLocationCode': arrcode,
        'guestTypes%5B0%5D.amount': '1',
        'guestTypes%5B1%5D.amount': '0',
        'guestTypes%5B2%5D.amount': '0',
        'discount': 'HTTP/1.1'
    }
    ret1 = session.get(url1, headers=headers1, params=data)

    headers2 = {
        'Host': 'www.airchangan.com',
        'Connection': 'keep-alive',
        'Content-Length': '15',
        'Origin': 'http://www.airchangan.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'Referer': url1,
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    data = {'ajaxAction': True}
    url2 = 'http://www.airchangan.com/InternetBooking/AirLowFareSearchExt.do'
    ret2 = session.post(url2, headers=headers2, data=data)

    url3 = 'http://www.airchangan.com/InternetBooking/AirFareFamiliesFlexibleForward.do'
    headers3 = {
        'Host': ' www.airchangan.com',
        'Connection': ' keep-alive',
        'Upgrade-Insecure-Requests': ' 1',
        'User-Agent': ' Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36',
        'Accept': ' text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': url1,
        'Accept-Encoding': ' gzip, deflate, sdch',
        'Accept-Language': ' zh-CN,zh;q=0.8'
    }
    cookie = requests.utils.dict_from_cookiejar(session.cookies)
    ret3 = session.get(url2, headers=headers3)
    return cookie, headers3, url3 + '?' + sel_date + depcode + arrcode
