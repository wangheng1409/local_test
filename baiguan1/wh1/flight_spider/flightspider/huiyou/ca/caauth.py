#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'fly'

import random
import requests
import urllib
import uuid
import simplejson

from flightspider.lib import tools, test_modify_router
from flightspider.log.sentry_log import log
from authenticity_token import AppAuthenticityToken
from device_context_piggybacker import DeviceContextPiggybacker


def ca_authentication(start_urls, http_proxy):
    """
    中国国航加密认证
    """
    # try:
    proxies = {"https": http_proxy, "http": http_proxy}
    device_id = str(uuid.uuid1())

    firmware_versions = ["ONE A2001_14_160418", "JSS153.I9300ZUMML1", "71CDBLB2297M", "AB160418", "5B16P18"]
    sdks = [{"sdk": "SDK 22", "os": "5.1.1"}, {"sdk": "SDK 17", "os": "4.2.2"}, {"sdk": "SDK 16", "os": "4.1.1"},
            {"sdk": "SDK 18", "os": "4.3"}, {"sdk": "SDK 19", "os": "4.4.4"},{"sdk": "SDK 21", "os": "5.0.0"},
            {"sdk": "SDK 23", "os": "6.0.0"}]
    model = tools.random_model()
    firmware_version = random.choice(firmware_versions)
    sdk = random.choice(sdks)
    user_agent = "WLNativeAPI(%s; %s; %s; %s; %s)" % (tools.random_str(8), firmware_version, model, sdk["sdk"], sdk["os"])
    headers = {"Accept-Language": "zh_CN",
                    # "User-Agent": "WLNativeAPI(OnePlus2; ONE A2001_14_160418; ONE A2001; SDK 22; Android 5.1.1)",
                    "User-Agent": user_agent,
                    "X-Requested-With": "XMLHttpRequest",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "x-wl-analytics-tracking-id": str(uuid.uuid1()),
                    "x-wl-app-version": "1.0",
                    "x-wl-clientlog-appname": "AirChina",
                    "x-wl-clientlog-appversion": "1.0",
                    "x-wl-clientlog-deviceId": device_id,
                    "x-wl-clientlog-env": "Android",
                    "x-wl-clientlog-model": model,
                    "x-wl-clientlog-osversion": sdk["os"],
                    "x-wl-platform-version": "6.3.0.0"
                    }
    # 生成设备号
    dcx = DeviceContextPiggybacker()
    device = dcx.get_message()
    params = {
        "parameters": "[{\"req\":\"{\\\"version \\\":\\\"1\\\"}\",\"lang\":\"zh_CN\",\"token\":\"11111111\"}]",
        "procedure": "hasUpgrade",
        "__wl_deviceCtx": device,
        "adapter": "ACCommon",
        "compressResponse": "false",
        "isAjaxRequest": "true",
        "x": "%s68378" % str(random.random())[0:13]
    }
    data = urllib.urlencode(params)
    req = requests.Session()
    print "!!!!!!!!!!!!!!!!"
    response = req.post(start_urls, data=data, headers=headers, verify=False, proxies=proxies)
    print ">>>>>>>>>>>>>>>>>>"
    if response.status_code in [403]:
        test_modify_router.dial()

    cookies = tools.cookie_2_dict(response.cookies)
    restext = response.text[11:][:-2]
    log.debug(restext)

    res_dict = eval(restext)
    wl_challenge_data = res_dict["challenges"]["wl_authenticityRealm"]["WL-Challenge-Data"]
    wl_instance_id = res_dict["challenges"]["wl_antiXSRFRealm"]["WL-Instance-Id"]
    token = res_dict["challenges"]["wl_deviceNoProvisioningRealm"]["token"]
    # 截取+号之前的数据
    challenge_data_str = wl_challenge_data.split("+")[0]
    # 加密逻辑
    at = AppAuthenticityToken()
    realm = at.a1("com.rytong.airchina", challenge_data_str)

    # 拼接关键认证数据
    auth_str = "{\"wl_deviceNoProvisioningRealm\":{\"ID\":{\"device\":{\"id\":\"" + device_id \
               + "\",\"os\":\"" + sdk["os"] + "\",\"model\":\"" + model + "\",\"environment\":\"Android\"},\"token\":\"" + token \
               + "\",\"app\":{\"id\":\"AirChina\",\"version\":\"1.0\"}}},\"wl_authenticityRealm\":\"" + realm + "\"}"

    headers["x-wl-analytics-tracking-id"] = str(uuid.uuid1())
    headers["WL-Instance-Id"] = wl_instance_id
    headers["Authorization"] = auth_str
    headers["Cookie2"] = "$Version=1"
    params["x"] = "%s6837" % random.random()
    nvps2 = urllib.urlencode(params)
    response = req.post(start_urls, data=nvps2, headers=headers, cookies=response.cookies, verify=False, proxies=proxies)
    rst = simplejson.loads(response.text[11:][:-2])
    log.debug(rst)
    if response.status_code in [403]:
        test_modify_router.dial()
    if rst.get("statusCode", 0) == 200 and rst.get("isSuccessful", ""):
        return [headers, cookies, params]
    #     log.error(rst)
    # except Exception, e:
    #     log.exception(e)
    # return []


if __name__ == "__main__":
    ca_authentication("https://m.airchina.com.cn:9061/worklight/apps/services/api/AirChina/android/query", "http://223.152.214.164:31009")