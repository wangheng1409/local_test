#!/usr/bin/env python
# -*-coding:utf-8-*-
import os
import time
import urllib
import base64
import requests
from rk import get_verification_code


def verificatin_code_cookie(sel_date, depcode, arrcode):
    # 申请验证码cookie
    code_url = 'http://www.fuzhou-air.cn/flight/searchflight.action?tripType=ONEWAY&orgCity1' \
               '=%s&dstCity1=%s&flightdate1=%s&flightdate2=&adult=1&child=0&infant=0' % (depcode, arrcode, sel_date)
    cookie_url = 'http://www.fuzhou-air.cn/hnatravel/signcode.jsp?flag=0&redirect=' + urllib.quote(base64.b64encode(code_url), '')

    print "申请验证码cookie"
    header1 = {
        "Host": "www.fuzhou-air.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Accept": "text/html, application/xhtml+xml, */*",
        "Accept-Language": "zh-CN",
        "Accept-Encoding": "gzip, deflate",
        "Referer": "http://www.fuzhou-air.cn/",
        "Connection": "keep-alive",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    cookie_rtn = requests.get(cookie_url, headers=header1)
    cookie = requests.utils.dict_from_cookiejar(cookie_rtn.cookies)
    # 验证码头部
    header = {
        "Host": "www.fuzhou-air.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Accept": "image/png, image/svg+xml, image/*;q=0.8, */*;q=0.5",
        "Accept-Language": "zh-CN",
        "Accept-Encoding": "gzip, deflate",
        "Referer": cookie_url,
        "DNT": "1",
        "Cookie": "JSESSIONID=" + cookie["JSESSIONID"],
        "Connection": "keep-alive"
    }
    url = 'http://www.fuzhou-air.cn/hnatravel/imagecode'
    rtn = requests.get(url, headers=header).content
    # 生成文件名
    file_name = 'fu_img_%d' % int(time.time())
    # 保存验证码图片
    with open(r'/home/kyfw/spider_tmp_data/fu_pic/%s.jpeg' % file_name, 'w') as f:
        f.write(rtn)
        f.close()
    print "*************"
    # {u'Result': u'mbrxk', u'Id': u'97cd905d-b35e-4dd6-a2c5-5dede6acde57'}
    ver_rtn = get_verification_code(r'/home/kyfw/spider_tmp_data/fu_pic/%s.jpeg' % file_name)
    result_code = ver_rtn["Result"]
    print result_code
    # 改验证码文件名
    os.rename(r'/home/kyfw/spider_tmp_data/fu_pic/%s.jpeg' % file_name, r'/home/kyfw/spider_tmp_data/'
                                                                        r'fu_pic/%s.jpeg' % result_code)
    # 删除验证码图片
    # filename = r'/home/kyfw/spider_tmp_data/fu_pic/%s.jpeg' % result_code
    # if os.path.exist(filename):
    #     os.remove(filename)

    # first
    headers = {
        "Host": "www.fuzhou-air.cn",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Accept": "*/*",
        "DNT": "1",
        "Referer": cookie_url,
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8",
    }
    first_url = 'http://www.fuzhou-air.cn/favicon.ico'
    first_request = requests.get(first_url, headers=headers)
    first_cookie = requests.utils.dict_from_cookiejar(first_request.cookies)

    # 请求验证码cookie sso_sign_eking
    header_sso = {
        "Host": "www.fuzhou-air.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Accept": "text/html, application/xhtml+xml, */*",
        "Accept-Language": "zh-CN",
        "Accept-Encoding": "gzip, deflate",
        "Referer": cookie_url,
        "DNT": "1",
        "Cookie": 'JSESSIONID='+cookie["JSESSIONID"]+';'
                   'JSESSIONID='+first_cookie["JSESSIONID"],
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Upgrade-Insecure-Requests": "1",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    str_datas = 'tickcode=' + result_code + "&redirect=" + urllib.quote(base64.b64encode(code_url), '') + '&flag=0&submit=%E6%8F%90%E4%BA%A4'
    url_sso = 'http://www.fuzhou-air.cn/hnatravel/checkSignCode'
    rtn_sso = requests.post(url_sso, headers=header_sso, data=str_datas, allow_redirects=False, timeout=20)
    sso_dict = requests.utils.dict_from_cookiejar(rtn_sso.cookies)
    cookies = {}
    cookies["sso_sign_eking"] = sso_dict["sso_sign_eking"]
    cookies["JSESSIONID"] = first_cookie["JSESSIONID"]
    return cookies
    #return sso_dict["sso_sign_eking"], first_cookie


def main():
    verificatin_code_cookie('', '2016-09-29', 'FOC', 'CSX')


if __name__ == '__main__':
    main()

