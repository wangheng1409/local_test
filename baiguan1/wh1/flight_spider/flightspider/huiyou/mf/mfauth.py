#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import time
import random
import urllib
from lxml import etree

from js_parse import JSRuntime


def mf_authentication(depcode, arrcode, sel_date):
    # 请求最开始的三个cookie JSESSIONID Webtrends BIGipServerpool_122.119.114.103
    head_cookie = {
        "X-Powered-By": "JSP/2.2",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",
        "Content-Type": "text/html;charset=UTF-8",
        "Content-Language": "zh-CN",
        "X-Via": "1.1 shjcl76:5 (Cdn Cache Server V2.0), 1.1 yangwtong49:5 (Cdn Cache Server V2.0)",
        "Connection": "keep-alive",
    }
    url_cookie = 'http://et.xiamenair.com/xiamenair/book/findFlights.action?tripType=0' \
                 '&queryFlightInfo=%s,%s,%s' % (depcode, arrcode, sel_date)
    rtn = requests.get(url_cookie, headers=head_cookie)
    cookie = requests.utils.dict_from_cookiejar(rtn.cookies)

    # 取页面的random值
    e_rtn = etree.HTML(rtn.text)
    r = e_rtn.xpath('//html/body/input[@id="random"]')[0].attrib['value']

    time_tmp = int(time.time())
    time_info = int(time_tmp * 1000) + random.randint(100, 999)

    # WT_FPC
    wt = "2"
    for item in xrange(18):
        wt += str(hex(random.randint(0, 15)))[-1]
    wt = wt + str(time_info) + ":lv=" + str(time_info) + ":ss=" + str(time_info)
    cookie["WT_FPC"] = wt

    # cookie ref id ses
    _pk_ref17ca2_str = r'["","",%s,"http://www.xiamenair.com/zh-cn/"]' % time_tmp
    _pk_ref17ca2 = urllib.quote(_pk_ref17ca2_str, "")
    cookie["_pk_ref.1.7ca2"] = _pk_ref17ca2

    js_obj = JSRuntime
    list_pk = js_obj._pk_id("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0")
    _pk_id17ca2 = "%s.%s.0.%s.%s.; " % (list_pk[0], int(list_pk[1]) / 1000,
                                        int(list_pk[1]) / 1000 + 1, int(list_pk[1]) / 1000)
    cookie["_pk_id.1.7ca2"] = _pk_id17ca2

    _pk_ses17ca2 = "*"
    cookie["_pk_ses.1.7ca2"] = _pk_ses17ca2

    return cookie, r, time_info
