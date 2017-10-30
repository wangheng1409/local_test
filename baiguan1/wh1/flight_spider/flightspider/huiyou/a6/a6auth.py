#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import urllib
import time
import random
from flightspider.lib.tools import getdayofday


def auth(depcode, arrcode, sel_date):
    # 获取cookie
    cookie = {}
    while True:
        params = {
            "orgCity": "%s" % depcode,
            "dstCity": "%s" % arrcode,
            "flightDate": "%s" % sel_date
        }
        param_encode = urllib.urlencode(params)
        url_cookie = 'http://www.redair.cn/booking/toShowFlight'
        cookie_rtn = requests.post(url_cookie, data=param_encode).cookies
        cookies = requests.utils.dict_from_cookiejar(cookie_rtn)
        if cookies.has_key("acw_tc") and cookies.has_key("JSESSIONID"):
            cookie = cookies
            break

    # header
    header = {
        "Host": "www.redair.cn",
        "Connection": "keep-alive",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/53.0.2785.143 Safari/537.36",
        "Referer": "http://www.redair.cn/booking/toShowFlight",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Cookie": "acw_tc=" + cookie["acw_tc"] + "; " + "JSESSIONID=" + cookie["JSESSIONID"]
    }

    # params
    time_tmp = int(time.time()) * 1000 + random.randint(100, 999)
    url_param = {
        "airwayType": "DC",
        "orgCity": "%s" % depcode,
        "dstCity": "%s" % arrcode,
        "flightDate": "%s" % sel_date,
        "lowerPriceParams": "",
        "_": "%s" % time_tmp
    }
    url_param_encode = urllib.urlencode(url_param)

    # url
    url = 'http://www.redair.cn/booking/ajaxFlightSearch?' + url_param_encode
    return cookie, header, url
