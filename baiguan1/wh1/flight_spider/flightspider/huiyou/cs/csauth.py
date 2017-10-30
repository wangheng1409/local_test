#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'fly'

import uuid
import urllib
import time
import requests

from flightspider import settings
from flightspider.lib import tools
from flightspider.log.sentry_log import log


def cs_authentication(http_proxy):
    """
    中国南方航空建立session
    """
    proxies = {"https": http_proxy, "http": http_proxy}
    start_urls = "http://3g.csair.com/CSMBP/data/homePage/getLaunchInfoNew.do?"
    model = tools.random_model()
    headers = {
        "Tingyun_Process": "true",
        "Charset": "UTF-8",
        "Content-Type": "text/xml; charset=UTF-8",
        "Connection": "Keep-Alive",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; %s Build/LMY47V) " % model,
        "Accept-Encoding": "zip",
    }

    dev_id = "ffffffff" + str(uuid.uuid1())[8:]
    params = {"APPTYPE": "android",
              "type": "mobile",
              "timestamp": "%d236" % int(time.time()),
              "gzip": "true",
              "appversionlog": "2.8.2.20160524",
              "deviceidlog": dev_id,
              "DEVICEID": dev_id,
              "oslog": "android",
              "osversionlog": "5.1.1",
              "APPVERSION": "2.8.2.20160524",
              "DEVICETYPE": model,
              "SYSTEMVERSION": "5.1.1",
              "lang": "zh",
              "LANGTYPE": "zh",
              # "PUSHTOKEN": "fdf26ef7eec4212640beb28bf87ec7f252fdc14b",
              "token": dev_id.replace("-", "")
              }

    req = requests.Session()
    url = start_urls + urllib.urlencode(params)
    max_trites = 3
    tries = 0
    cookies = None
    while True:
        response = req.post(url, headers=headers, proxies=proxies, timeout=settings.DOWNLOAD_TIMEOUT)
        try:
            cookies = tools.cookie_2_dict(response.cookies)
        except:
            if tries < max_trites:
                tries += 1
                continue
            raise response.cookies
        break
    return [headers, cookies, params]

