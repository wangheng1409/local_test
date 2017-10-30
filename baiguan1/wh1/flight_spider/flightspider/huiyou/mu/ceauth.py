#!/usr/bin/python
# -*-coding:utf-8-*-
__author__ = "fly"

import base64
import gzip
import random
import time
import os
import urllib

import requests
from Crypto.Cipher import AES
from M2Crypto import RSA, X509
from StringIO import StringIO

import dec_data
import hmac_utils

from flightspider import settings
from flightspider.lib import tools
from flightspider.log.sentry_log import log

BS = AES.block_size
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[0:-ord(s[-1])]


class MobileMu(object):
    """
    模拟东航手机客户端
    """

    def __init__(self):
        self.serverHelloBody_ = None
        self.clientHelloBody_ = None
        self.ex_hander = None

        self.imei = tools.random_str(15, "0123456789")
        self.model = tools.random_model()
        mac = tools.random_mac()
        self.sdk = random.choice([17, 18, 19, 20, 21, 22])  # 随机生成android sdk 版本
        resolutions = ["1280*720", "1920*1080", "854*480", "960*540", "800*480", "1184*720", "1776*1080", "1280*800",
                       "1800*1080"]
        self.resolution = random.choice(resolutions)
        self.network_type = random.choice(["wifi", "4G"])
        self.device_data = {
            'ostype': 'and',
            'imei': self.imei,
            'mac': mac,
            'model': self.model,
            'sdk': self.sdk
        }
        self.timeDifference = 0L
        self.deviceinfo = "".join(["&%s=%s" % (k, v) for k, v in self.device_data.items()])
        self.rad = random.randint(0, 999) % 900 + 100
        self.headers = {"Accept": "text/vnd.wap.wml",
                        "User-Agent": "LightPole/5.6.0/android1.5",
                        "Pragma": "no-cache",
                        "Connection": "Keep-Alive",
                        "Accept-Encoding": "gzip,deflate",
                        "Content-Type": "application/x-www-form-urlencoded"}

        self.url_params = {"app": "ceair",
                           "o": "i"}

        self.retry_times = 0

    def authentication(self, http_proxy):

        proxies = {"http": http_proxy}
        params = dec_data.checkcode(self.timeDifference, self.deviceinfo, "client_version=&plantform=AD")
        start_urls = "http://mobile.ceair.com/user/tmstp?%s" % urllib.urlencode(self.url_params)
        response = requests.post(start_urls, data=params, headers=self.headers, timeout=settings.DOWNLOAD_TIMEOUT,
                                 proxies=proxies)
        de_res = dec_data.decheckcode(response.text).strip()

        if "ewp_proxy_err_msg=" not in de_res:
            self.timeDifference = long(de_res) - long(time.time() * 1000)
        body = self.createfullclienthellobody()
        self.clientHelloBody_ = body
        self.url_params["ota_version"] = "AD-UMP-5.6.0-080901"
        self.url_params["clientinfo"] = "android-%s-%s-5.6.0-JOP40D" % (self.sdk, tools.random_str(5))
        start_urls2 = "http://mobile.ceair.com/user/hello?%s" % urllib.urlencode(self.url_params)
        body_se = [chr(body[i]) for i in range(0, len(body))]
        params = base64.b64encode("".join(body_se))
        response = requests.post(start_urls2, data=params, headers=self.headers, timeout=settings.DOWNLOAD_TIMEOUT, proxies=proxies)
        response.encoding = "ISO-8859-1"
        ret = response.text

        data2 = [ord(ret[i]) for i in range(0, len(ret))]
        self.serverHelloBody_ = data2
        self.handleserverhello(data2, 0)
        array1 = self.getclientkeyexchangebody() + [7, 0, 0, 0, 1, 0]
        array6 = array1 + self.getfinishbody(self.clientHelloBody_ + self.serverHelloBody_ + array1)
        temp = [chr(array6[i]) for i in range(0, len(array6))]
        str2 = base64.b64encode("".join(temp))
        key_url_pararm = {"imei": encode(self.imei, "czbankmobile"),
                          "checkkey": encode_imei(self.imei, self.rad),
                          "lfrn": str(self.rad),
                          "pwdautologin": "",
                          "logintype": "",
                          "deviceModel": self.model,
                          "is_install_samsung_wallet": "false",
                          "channelType": "M360",
                          "hasOrNotBroken": 0,
                          "telecomOperator": "",
                          "networkType": self.network_type,
                          "resolution": self.resolution,
                          "location_city": ""
                          }

        start_urls3 = "http://mobile.ceair.com/user/exchange?%s" % urllib.urlencode(
            dict(key_url_pararm.items() + self.url_params.items()))
        params = dec_data.checkcode(self.timeDifference, self.deviceinfo, str2)
        self.ex_hander = self.headers
        self.ex_hander["X-Emp-Cookie"] = self.cookie
        self.ex_hander["Cookie"] = self.cookie
        response = requests.post(start_urls3, data=params, headers=self.ex_hander,
                                 timeout=settings.DOWNLOAD_TIMEOUT, proxies=proxies)
        response.encoding = "ISO-8859-1"
        ret = response.text
        resp = [ord(ret[i]) for i in range(0, len(ret))]
        ms2_, array11 = self.handlerserverkeyexchange(resp, 0)
        self.getfinalkey(ms2_, array11)



    # def query(self, orgCode="PEK", dstCode="SHA", selDate="20160606"):
    #     requrl = "http://mobile.ceair.com/app_s/act/ch_jpyd/bang_bang?app=ceair&o=i"
    #     msg = "orgCode=" + orgCode + "&dstCode=" + dstCode + "&departDate=" + selDate + "&timeBucket=0&cabin=0&n=tms.do%3ftranCode%3dTM0500&flag=0&sortRule=1&tripType=1&isQueryOd=true&searchType=XYX&isUseNewdesc=true&isQueryGift=TRUE" + "&twozip=1"
    #
    #     clientkeystr = "".join([chr(self.clientKey_[i]) for i in range(0, len(self.clientKey_))])
    #     clientivstr = "".join([chr(self.clientIv_[i]) for i in range(0, len(self.clientIv_))])
    #     cipher = AES.new(clientkeystr, AES.MODE_CBC, clientivstr)
    #     params = base64.b64encode(cipher.encrypt(pad(msg)))
    #
    #     msg_b = [ord(params[i]) for i in range(0, len(params))]
    #     signhex = hmac_utils.encrypt_hmac(msg_b, self.clientHmacKey_, "HmacSHA1")
    #     signdata = hexstr2intarray(signhex)
    #     signstr = ""
    #     for i in range(0, len(signdata)):
    #         signstr += chr(signdata[i])
    #     sign = base64.b64encode(signstr)
    #
    #     self.ex_hander["X-Emp-Signature"] = sign
    #     response = requests.post(requrl, data=params, headers=self.ex_hander)
    #     response.encoding = "ISO-8859-1"
    #     ret = response.text
    #
    #     serverkeystr = "".join([chr(self.serverKey_[i]) for i in range(0, len(self.serverKey_))])
    #     serverivstr = "".join([chr(self.serverIv_[i]) for i in range(0, len(self.serverIv_))])
    #     cipher = AES.new(serverkeystr, AES.MODE_CBC, serverivstr)
    #     ret = unpad(cipher.decrypt(base64.b64decode(ret)))
    #
    #     buf = StringIO(ret)
    #     f = gzip.GzipFile(fileobj=buf, mode="rb")
    #     ret = f.read()
    #     # print ret.strip()
    #     # print simplejson.loads(ret.strip())

    def handleserverhello(self, data, paramint):
        i = data[paramint]
        j = paramint + 1
        k = j + 4
        if i != 2:
            return k
        array1 = data[(k + 2):(k + 2 + 32)]
        self.RNS_ = array1
        i1 = k + 34
        i2 = data[i1]
        i3 = i1 + 1
        array2 = data[i3:(i3 + i2)]
        i4 = i3 + i2
        array3 = [chr(array2[x]) for x in range(0, len(array2))]
        self.cookie = "_session_id=" + dec_data.decheckcode("".join(array3))
        return i4 + 2

    def createfullclienthellobody(self):
        array1 = [1, 0]
        self.RNC_ = getclienttime() + getclientrandom(28)
        array2 = [0, 0, 4, 0, 7, 0, 6, 0]
        array3 = array1 + self.RNC_ + array2
        array4 = inttobytearrayinnbo(len(array3))
        return [1] + array4 + array3

    def getclientkeyexchangebody(self):
        array1 = [1, 0] + getclientrandom(46)
        self.PMS_ = array1
        src_data = array1 + self.RNS_ + [0]
        srcstr = "".join([chr(src_data[i]) for i in range(0, len(src_data))])
        cert = X509.load_cert(os.path.join(settings.FINAL_TABLE_PATH, "mu/keytables/cer.txt"), X509.FORMAT_DER)
        pubkey = cert.get_pubkey().get_rsa()
        en_ret = pubkey.public_encrypt(srcstr, RSA.pkcs1_padding)
        array2 = [ord(en_ret[i]) for i in range(0, len(en_ret))]
        return [9] + inttobytearrayinnbo(len(array2)) + array2

    def getfinishbody(self, data):
        str1 = "client finished"
        array1 = [ord(str1[i]) for i in range(0, len(str1))]
        str2 = "".join([chr(data[i]) for i in range(0, len(data))])
        temp = hmac_utils.md5(str2)
        array2 = hexstr2intarray(temp)
        temp = hmac_utils.sha1(str2)
        array3 = hexstr2intarray(temp)
        array4 = array2 + array3
        array5 = self.PMS_
        str3 = "master secret"
        array6 = [ord(str3[i]) for i in range(0, len(str3))]
        array7 = hmac_utils.prf(array5, array6, (self.RNC_ + self.RNS_), 68)
        self.MS_ = array7
        array1 = hmac_utils.prf(array7, array1, array4, 12)
        return [10] + inttobytearrayinnbo(len(array1)) + array1

    def getfinalkey(self, data1, data2):
        tempstr = "key expansion"
        temparray = [ord(tempstr[i]) for i in range(0, len(tempstr))]
        array1 = hmac_utils.prf(data1, temparray, data2, 136)
        array2 = array1[0:68]
        array3 = array1[68:68 + 68]
        self.clientKey_ = array2[0:32]
        self.clientIv_ = array2[32:48]
        self.serverKey_ = array3[0:32]
        self.serverIv_ = array3[32:48]
        self.clientHmacKey_ = array2[48:68]

    def getfinishbody(self, data):
        str1 = "client finished"
        array1 = [ord(str1[i]) for i in range(0, len(str1))]
        str2 = "".join([chr(data[i]) for i in range(0, len(data))])
        temp = hmac_utils.md5(str2)
        array2 = hexstr2intarray(temp)
        temp = hmac_utils.sha1(str2)
        array3 = hexstr2intarray(temp)
        array4 = array2 + array3
        array5 = self.PMS_
        str3 = "master secret"
        array6 = [ord(str3[i]) for i in range(0, len(str3))]
        array7 = hmac_utils.prf(array5, array6, (self.RNC_ + self.RNS_), 68)
        self.MS_ = array7
        new_array = hmac_utils.prf(array7, array1, array4, 12)
        return [10] + inttobytearrayinnbo(len(new_array)) + new_array

    def handlerserverkeyexchange(self, data, paramint):
        i = data[paramint]
        j = paramint + 1
        array1 = data[j:j + 4]
        k = j + 4
        m = bytearraytointinnbo(array1, 0)
        if i == 5:
            data = data[k:k + m]
            array1 = self.MS_
            aeskey = array1[0:32]
            aesiv = array1[32:48]
            aeskeystr = "".join([chr(aeskey[i]) for i in range(0, len(aeskey))])
            aesivstr = "".join([chr(aesiv[i]) for i in range(0, len(aesiv))])
            datastr = "".join([chr(data[i]) for i in range(0, len(data))])
            cipher = AES.new(aeskeystr, AES.MODE_CBC, aesivstr)
            destr = unpad(cipher.decrypt(datastr))
            array2 = [ord(destr[i]) for i in range(0, len(destr))]
            array5 = array2[32:32 + 2]
            array6 = array2[34:34 + 46]
            array9 = array5 + array6
            array11 = self.RNC_ + self.RNS_
            tempstr = "master secret2"
            temparray = [ord(tempstr[i]) for i in range(0, len(tempstr))]
            ms2_ = hmac_utils.prf(array9, temparray, array11, 48)
            k += m
        return ms2_, array11


def inttobytearrayinnbo(paramint):
    data = [0] * 4
    for i in range(0, 4):
        data[i] = (paramint >> 24 - i * 8) & 0xFF
    return data


def getclienttime():
    current_time = time.localtime(time.time())
    hour = int(time.strftime("%H", current_time))
    minute = int(time.strftime("%M", current_time))
    client_time = [0] * 4
    client_time[0] = int((hour & 0xFF00) >> 8)
    client_time[1] = int(hour & 0xFF)
    client_time[2] = int((minute & 0xFF00) >> 8)
    client_time[3] = int(minute & 0xFF)
    return client_time


def bytearraytointinnbo(data, paramint):
    i = 0
    for j in range(0, 4):
        k = 8 * (3 - j)
        i += ((0xFF & data[(j + paramint)]) << k)
    return i


def getclientrandom(paramint):
    data = [0] * paramint
    for i in range(0, paramint):
        data[i] = int(((long(time.time() * 1000) + random.randint(-231, 230) % 256L) & 0xFF))
    return data


def hexstr2intarray(p_str):
    arraylen = len(p_str) / 2
    array = []
    for i in range(0, arraylen):
        temp = p_str[i * 2:i * 2 + 2]
        array.append(int(temp, 16))
    return array


def encode(p_str1, p_str2):
    data1 = [ord(p_str1[i]) for i in range(0, len(p_str1))]
    data2 = [ord(p_str2[i]) for i in range(0, len(p_str2))]
    temparray = xorwithkey(data1, data2)
    temp = "".join([chr(temparray[i]) for i in range(0, len(temparray))])
    return base64.b64encode(temp)


def encode_imei(p_str, paramint):
    if len(p_str) > 0:
        str1 = p_str[0:1] + "5" + p_str[2:]
        i = len(str1) / 2
        str2 = str1[0:i] + str1[len(str1) - 1:] + str1[i + 1:]
        str3 = str(bin(paramint % 10))
        if len(str3) < 4:
            while 4 - len(str3) > 0:
                str3 = "0" + str3
        return base64.b64encode(str2 + str3)
    else:
        return ""


def xorwithkey(data1, data2):
    array = [0] * len(data1)
    for i in range(0, len(data1)):
        array[i] = data1[i] ^ data2[i % len(data2)]
    return array


if __name__ == "__main__":
    print len("864793026964077")
    # mu = MobileMu()
    # print "=================="
    # mu.authentication()
    # mu.query()
