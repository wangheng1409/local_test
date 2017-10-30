#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'fly'

import base64
import gzip
import urllib
import time

import simplejson
from Crypto.Cipher import AES
from StringIO import StringIO
from scrapy.http.request import Request
from scrapy.exceptions import CloseSpider

from flightspider import database
from flightspider.huiyou.mu import ceauth
from flightspider.huiyou.mu import hmac_utils
from flightspider.items import FlightSpiderDetailItem
from flightspider.lib.tools import getdayofday
from flightspider.log.sentry_log import log
from flightspider.lib import http_proxy
from flightspider.spiders.base_spider import BaseSpider

INVALID_MSG = u"ewp_proxy_err_msg=很抱歉，暂无通航该机场的航班。"

class CeDetailSpider(BaseSpider):
    """
    中国南方航班运价数据
    """
    name = "cedetail"
    code = "MU"
    allowed_domains = ["mobile.ceair.com"]
    start_urls = "http://mobile.ceair.com/app_s/act/ch_jpyd/bang_bang?app=ceair&o=i"
    handle_httpstatus_list = [500, 502, 503, 504, 400, 403, 404, 408]

    def start_requests(self):
        tasks = self.get_tasks(self.code)
        for task in tasks:
            dst = task["depCode"]
            org = task["arrCode"]
            cycle = task["spiderCycle"]
            dacode = task["name"]
            # 身份认证
            max_trites = 3
            tries = 0
            while True:
                try:
                    ce = ceauth.MobileMu()
                    ce.authentication(self.http_proxy)
                except Exception, e:
                    if tries < max_trites:
                        tries += 1
                        continue
                    exc = "%r:%r" % (Exception, e)
                    self.spider_exception("0000-00-00", dacode, "CE Authentioincation Exception", "request ce authentication", exc=exc)
                break

            for d in xrange(task["dateRange"]):
                # 计算有效航线
                sel_date, week = getdayofday(d, True)
                sel_date = sel_date.replace("-", "")
                if task["weeks"].find(week) < 0:
                    continue
                params_dict = {"orgCode": dst,
                               "dstCode": org,
                               "departDate": sel_date,
                               "timeBucket": 0,
                               "n": "tms.do?tranCode=TM0500",
                               "cabin": 0,
                               "flag": 0,
                               "sortRule": 1,
                               "tripType": 1,
                               "isQueryOd": "true",
                               "searchType": "XYX_b2g",
                               "isUseNewdesc": "true",
                               "isQueryGift": "TRUE",
                               "twozip": 1
                               }

                clientkeystr = "".join([chr(ce.clientKey_[i]) for i in range(0, len(ce.clientKey_))])
                clientivstr = "".join([chr(ce.clientIv_[i]) for i in range(0, len(ce.clientIv_))])
                cipher = AES.new(clientkeystr, AES.MODE_CBC, clientivstr)
                params = base64.b64encode(cipher.encrypt(ceauth.pad(urllib.urlencode(params_dict))))

                msg_b = [ord(params[i]) for i in range(0, len(params))]
                signhex = hmac_utils.encrypt_hmac(msg_b, ce.clientHmacKey_, "HmacSHA1")
                signdata = ceauth.hexstr2intarray(signhex)
                signstr = ""
                for i in range(0, len(signdata)):
                    signstr += chr(signdata[i])
                sign = base64.b64encode(signstr)
                ce.ex_hander["X-Emp-Signature"] = sign
                yield Request(self.start_urls, method="POST", body=params, headers=ce.ex_hander,
                              callback=self.parse_detail, meta={'date': sel_date, 'cycle': cycle, 'serverkey':
                        ce.serverKey_, 'serveriv': ce.serverIv_, "dst": dst, "org": org, "proxy": self.http_proxy,
                                                                'dacode': dacode})

    def parse_detail(self, response):
        """
        获取航班详细信息
        """
        ret = response.body
        serverkeystr = "".join(
            [chr(response.meta["serverkey"][i]) for i in range(0, len(response.meta["serverkey"]))])
        serverivstr = "".join([chr(response.meta["serveriv"][i]) for i in range(0, len(response.meta["serveriv"]))])
        cipher = AES.new(serverkeystr, AES.MODE_CBC, serverivstr)
        ret = ceauth.unpad(cipher.decrypt(base64.b64decode(ret)))
        buf = StringIO(ret)
        f = gzip.GzipFile(fileobj=buf, mode="rb")
        rst = f.read()
        flight_date = response.meta["date"]
        dacode = response.meta["dacode"]
        try:
            rst_str = simplejson.loads(rst)
        except Exception, e:
            sel_date = getdayofday()
            sel_date = sel_date.replace("-", "")
            if sel_date != flight_date:
                exc = "%r:%r:%s" % (Exception, e, rst)
                http_proxy.retry_http_proxy(self.hp_id)
                code = dacode.split("-")
                database.insert_fix_spider_policy("MU", dacode, code[0], code[1])
                self.spider_exception(flight_date, dacode, "IP Exception", "request CE flight detail error", exc=exc)
        if rst_str.get("flight_items", None):
            items = []
            for cabin in rst_str["flight_items"]:
                item = FlightSpiderDetailItem()
                item["flightNo"] = cabin["flightNo"]
                item["flightDate"] = flight_date
                item["cabinId"] = cabin.get("cabinCode")
                item["daCode"] = response.meta["dacode"]
                if cabin.get("fdPrice", ""):
                    item["vipPrice"] = int(cabin.get("price"))
                else:
                    item["price"] = int(cabin.get("price"))
                item["priceCurrency"] = "CNY"
                item["share"] = 0
                if cabin["codeShareCarriar"] != "MU":
                    item["share"] = 1
                # item["surplusTicket"] = -1
                # if cabin.get("seatNumber") != "A":
                #     item["surplusTicket"] = int(cabin.get("seatNumber"))
                item["surplusTicket"] = cabin.get("seatNumber")
                item["remarks"] = simplejson.dumps({"descOrder": cabin.get("descOrder")})
                item["syncCycle"] = response.meta["cycle"]
                items.append(item)
            return items
        else:
            msg = "%s:%s:%s" % (flight_date, dacode, rst)
            log.info(msg)

    def spider_exception(self, flight_date, dacode, reason, msg, errcode=-1, exc=""):
        self.tmp_retry_tiems = errcode
        http_proxy.retry_http_proxy(self.hp_id)
        log.error("%s %s %s %s" % (msg, flight_date, dacode, exc))
        raise CloseSpider(reason)