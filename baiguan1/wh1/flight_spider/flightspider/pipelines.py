#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'fly'

from datetime import datetime

import database


class FlightSpiderBasePipeline(object):
    def process_item(self, item, spider):
        if spider.name in ['eubase', 'g5base']:
            insert_table = '%sflight_base' % item["company"].lower()
            sql = "replace into " + insert_table + " (flightNo, depcode, arrcode, company, season, planTime) " \
                                                   "values (%s, %s, %s, %s, %s, %s)"

            database.db.insert(sql, item['flightNo'], item['depcode'],
                               item['arrcode'], item['company'],
                               item['season'], item['depPlanTime'])

        elif spider.name in ['cabase', 'csbase']:
            sql = "replace into ca_flight_base (flightNo, depcode, arrcode, " \
                  "company, season, depPlanTime, arrPlanTime) values (%s, %s, %s, %s, %s, %s, %s)"

            database.db.insert(sql, item['flightNo'], item['depcode'], item['arrcode'], item['company'], item['season'],
                               item['depPlanTime'], item['arrPlanTime'])
        else:
            return item


class FlightSpiderDetailPipeline(object):
    """
    flightNo,flightDate,cabinId三个为联合主键
    1. detail表记录存在并且无变化，更新syncTime
    2. detail表记录存在余票数和票价有变化，更新票价和余票数，并将更新前的记录保存到history表
    3. detail表不存记录插入
    """

    def process_item(self, item, spider):
        if spider.name not in ['cadetail', 'csdetail', 'cedetail', 'eudetail', 'g5detail', 'jrdetail', 'mfdetail',
                               'tvdetail', 'fudetail', 'uqdetail', 'nsdetail', 's_9hdetail','bkdetail']:
            return item

        sel_sql = "select * from flight_detail where flightNo=%s and " \
                  "flightDate=%s and cabinId=%s and depCode=%s and arrCode=%s;"

        rst = database.db.query(sel_sql, item['flightNo'], item['flightDate'], item['cabinId'], item['depCode'],
                                item["arrCode"])
        if rst:
            if len(rst) > 1:
                for r in rst[:-1]:
                    database.db.execute_rowcount("delete from flight_detail where id=%s", r['id'])
                rst = rst[:-1][0]
            else:
                rst = rst[0]

        tmp_price = price = item.get('price', None)
        vip_price = item.get('vipPrice', None)
        tmp_field = "price"
        if vip_price:
            tmp_field = "vipPrice"
            tmp_price = vip_price
        if rst:
            if rst.get("price") != int(price) or rst.get("vipPrice") != vip_price\
                    or rst.get("surplusTicket") != item['surplusTicket']:
                #  有变化则更新价格或者余票
                up_sql = "update flight_detail set " + tmp_field +\
                         "=%s, surplusTicket=%s where flightNo=%s and" \
                         " flightDate=%s and cabinId=%s and depCode=%s and arrCode=%s; "

                database.db.update(up_sql, tmp_price, item['surplusTicket'], item['flightNo'], item['flightDate'],
                                   item['cabinId'], item['depCode'], item['arrCode'])

                in_history_sql = "insert into flight_detail_history(company, flightNo, " \
                                 "flightDate, cabinId, depCode, arrCode, " + tmp_field + \
                                 ", priceCurrency, surplusTicket, share, remarks) values " \
                                 "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

                database.db.insert(in_history_sql, rst['company'], rst['flightNo'], rst['flightDate'],
                                   rst['cabinId'], item['depCode'], item['arrCode'], rst[tmp_field],
                                   rst['priceCurrency'], rst['surplusTicket'], rst['share'], rst['remarks'])
            else:
                # 价格和余票没有变化更新syncTime
                up_sql = "update flight_detail set syncTime=%s where flightNo=%s " \
                         "and flightDate=%s and cabinId=%s and depCode=%s and arrCode=%s; "

                database.db.update(up_sql, str(datetime.now()), item['flightNo'], item['flightDate'],
                                   item['cabinId'], item['depCode'], item['arrCode'])
        else:
            in_sql = "insert into flight_detail (company, flightNo, flightDate, cabinId, " \
                     "depCode, arrCode, " + tmp_field + ", priceCurrency, surplusTicket," \
                                                        " share, remarks, syncCycle) values " \
                                                        "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            database.db.insert(in_sql, item['company'], item['flightNo'], item['flightDate'], item['cabinId'],
                               item['depCode'], item['arrCode'], tmp_price, item['priceCurrency'],
                               item['surplusTicket'], item['share'], item['remarks'], item['syncCycle'])
