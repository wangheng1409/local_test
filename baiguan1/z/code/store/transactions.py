# -*- coding: utf-8 -*-
from lxml import etree
import hashlib
import random
import json
import types
import sys
import requests
import xmltodict


WECHAT_UNIFIED_ORDER_URL = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
WECHAT_DOWNLOAD_BILL_URl = 'https://api.mch.weixin.qq.com/pay/downloadbill'
WECHAT_ORDER_QUERY_URL = 'https://api.mch.weixin.qq.com/pay/orderquery'


ALIPAY_GATEWAY_URL = 'https://mapi.alipay.com/gateway.do'
SERVICE_SINGLE_TRADE_QUERY = 'single_trade_query'
SERVICE_ACCOUNT_PAGE_QUERY = 'account.page.query'


GEN_STRING = 0
GEN_UNIFORM = 1

def dict2xml(data):
    xml = etree.Element('xml')
    for k, v in data.items():
        child = etree.Element(k) 
        child.text = etree.CDATA(json.dumps(v)) if type(v) is types.DictionaryType else v.decode('utf-8')
        xml.append(child)
    return etree.tostring(xml, encoding='utf-8')

def wechat_md5_sign(params, key):
    # params_sorted = [(k,params[k]) for k in sorted(params.keys())]
    params_sorted = sorted(params.items(), lambda x, y: cmp(x[0], y[0]))
    params_str = ''
    for param in params_sorted:
        params_str += '%s=%s&'%(param[0], json.dumps(param[1]) if type(param[1]) is types.DictionaryType else param[1])
    params_str = params_str[:-1]
    encryptor = hashlib.md5()
    encryptor.update('%s&key=%s'%(params_str, key))
    params['sign'] = encryptor.hexdigest().upper()
    return params

def alipay_md5_sign(params, key):
    params_sorted = sorted(params.items(), lambda x, y: cmp(x[0], y[0]))
    params_str = ''
    for param in params_sorted:
        params_str += '%s=%s&'%(param[0], param[1])
    params_str = params_str[:-1]
    encryptor = hashlib.md5()
    encryptor.update('%s%s'%(params_str, key))
    params['sign'] = encryptor.hexdigest()
    params['sign_type'] = 'MD5'
    return params


def gen_nonce_str():
    nonce_str = ''
    while len(nonce_str) < 32:
        nonce_str += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') if random.choice([GEN_STRING,GEN_UNIFORM])==GEN_UNIFORM else str(random.randint(0, 9))
    return nonce_str


class WeChatPaymentHelper():
    def __init__(self):
        pass

    @staticmethod
    def access_url(url, key, json_data=None, **kwargs):
        if json_data:
            signed_params = json.loads(json_data)
        else:
            signed_params = kwargs
        for k, v in signed_params.items():
            if not v:
                signed_params.pop(k)
        signed_params = wechat_md5_sign(signed_params, key)
        data = dict2xml(signed_params)
        print data
        r = requests.post(url, data=data)
        return xmltodict.parse(r.content)


class AlipayHelper():
    def __init__(self):
        pass

    @staticmethod
    def access_service(service, key, json_data=None, **kwargs):
        signed_params = json.loads(json_data) if json_data else kwargs
        signed_params['service'] = service
        for k, v in signed_params.items():
            if not v:
                signed_params.pop(k)
        signed_params = alipay_md5_sign(signed_params, key)
        print signed_params
        r = requests.get(ALIPAY_GATEWAY_URL, params=signed_params)
        return xmltodict.parse(r.content)

    @staticmethod
    def parse_page_query_response(response):
        content = xmltodict.parse(response)
        alipay = content.get('alipay')
        if alipay.get('is_success') == 'T':
            logs = alipay.get('response').get('account_page_query_result').get('account_log_list')
            logs = [dict(items) for log, items in logs.items()]
            return logs

