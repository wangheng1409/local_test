#!/usr/bin/python
# -*-coding:utf-8-*-
__author__ = "fly"


import time
import base64
import aes
import hmac_utils


def checkcode(timedifference, deviceinfo, content):
    current_time = long(time.time() * 1000)
    current_time += timedifference
    content += deviceinfo + "&serviceTime=" + str(current_time)
    md5_str = hmac_utils.md5(content)
    md5_result = ""
    for i in range(24, 32):
        md5_result += md5_str[i]
    for i in range(8, 24):
        md5_result += md5_str[i]
    for i in range(0, 8):
        md5_result += md5_str[i]
    content += "&checkcode=" + md5_result
    en_result = aes.en_data(content)
    for i in range(0, len(en_result)):
        en_result[i] = chr(en_result[i])
    result = "S" + base64.b64encode("".join(en_result))
    return result

def decheckcode(p_str):
    if p_str.startswith("S"):
        p_str = p_str[1:]
    tmp_result = []
    for i in base64.b64decode(p_str):
        tmp_result.append(ord(i))
    result = aes.de_data(tmp_result, iv=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    return result


