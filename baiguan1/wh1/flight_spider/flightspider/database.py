#!/usr/bin/python
# -*-coding:utf-8-*-
__author__ = "fly"

import random
import torndb
import settings

if settings.TEST_ENVIRONMENT:
    db = torndb.Connection(settings.DATABASE_TEST["host"], settings.DATABASE_TEST["database"],
                           settings.DATABASE_TEST["username"],
                           settings.DATABASE_TEST["password"],
                           time_zone="+8:00")
else:
    db = torndb.Connection(settings.DATABASE["host"], settings.DATABASE["database"], settings.DATABASE["username"],
                           settings.DATABASE["password"], time_zone="+8:00")


# ======================================================================
# 抓取策略相关
# ======================================================================


def get_all_tasks(offset=0, limit=30, company=None):
    """
    查询爬虫策略
    :param worker_name:
    :param spider_name:
    :param company:
    :return:
    """
    if company:
        sql = "SELECT id, spiderName FROM spider_policy WHERE company IN ('%s') and state=1 ORDER BY priority, id DESC " \
               "LIMIT %d OFFSET %d" % (company.replace(",", "','"), limit, offset)
        return db.query(sql)
    else:
        return db.query(
            "SELECT id, spiderName FROM spider_policy WHERE state=1 ORDER BY priority, id DESC LIMIT %s OFFSET %s",
            limit, offset)


def reset_spider_policy(company=None):
    """
    初始化每条策略抓取状态
    :return:
    """
    if company:
        sql = "UPDATE spider_policy SET work_desc='', work_state=0, data_count=0 WHERE " \
              "company IN ('%s') AND state=1" % company.replace(",", "','")
        return db.update(sql)
    else:
        return db.update("UPDATE spider_policy SET work_desc='', work_state=0, data_count=0 WHERE state=1")


def get_task_by_work_state(work_state=0, offset=0, limit=30, company=None):
    """
    根据爬虫状态获取任务列表
    :param work_state:
    :param offset:
    :param limit:
    :return:
    """
    if company:
        sql = "SELECT id, spiderName FROM spider_policy WHERE company IN ('%s') AND work_state=%s AND state=1 " \
              "ORDER BY priority, id DESC LIMIT %s OFFSET %s" % (company.replace(",", "','"), work_state, limit, offset)
        return db.query(sql)
    else:
        return db.query(
            "SELECT id, spiderName FROM spider_policy WHERE work_state=%s AND state=1 ORDER BY priority, id DESC "
            "LIMIT %s OFFSET %s", work_state, limit, offset)


def count_task_by_work_state(work_state=0, company=None):
    """
    根据爬虫状态获取统计数量
    :param work_state:
    :return:
    """
    if company:
        sql = "SELECT count(id) as `count` FROM spider_policy WHERE company IN ('%s') AND work_state IN (%s) AND " \
              "state=1 " % (company.replace(",", "','") , work_state)
        return db.get(sql)
    else:
        return db.get("SELECT count(id) as `count` FROM spider_policy WHERE work_state IN (%s) AND state=1", work_state)


def get_tasks(worker_name, spider_name, company, tid=-1):
    """
    查询爬虫策略
    :param worker_name:
    :param spider_name:
    :param company:
    :return:
    """
    if tid == -1:
        return db.query(
            "SELECT id, name, depCode, arrCode, spiderCycle, dateRange, weeks FROM spider_policy WHERE worker=%s AND "
            "spiderName=%s AND company=%s AND state=1 AND priority ORDER BY priority, id DESC ", worker_name, spider_name,
            company)
    else:
        return db.query("SELECT id, name, depCode, arrCode, spiderCycle, dateRange, weeks FROM spider_policy WHERE id=%s",
                        tid)


def update_task_state(policy_id, work_state):
    """
    修改抓取状态
    :param policy_id:
    :param work_state: 0未分配,1以分配,2已经开始抓取,3抓取完成,4抓取异常
    :return:
    """
    return db.update("UPDATE spider_policy SET work_state=%s WHERE id=%s", work_state, policy_id)


def update_task_record(policy_id, work_desc, state, data_count=0):
    """
    任务完成后更新抓取结果
    :param policy_id:
    :param work_desc:
    :return:
    """
    return db.update("UPDATE spider_policy SET work_desc=%s, work_state=%s, data_count=%s WHERE id=%s", work_desc, state,
                     data_count, policy_id)


def get_enabled_company():
    """
    获取所有启用策略航空公司
    :return:
    """
    return db.query("SELECT count(*) as count, company FROM `spider_policy` WHERE state=1 GROUP BY company")


def count_spider_flight(company=None):
    """
    统计抓取的数据量
    :param company:
    :return:
    """
    if company:
        return db.get("SELECT sum(data_count) as `count` FROM spider_policy WHERE company=%s", company)
    else:
        return db.get("SELECT sum(data_count) as `count` FROM spider_policy")


def insert_fix_spider_policy(company, name, depCode, arrCode, dateRange, spiderName, weeks):
    """
    :param company:
    :param name:
    :param depCode:
    :param arrCode:
    :param dateRange:
    :param spiderName:
    :param weeks:
    :return:
    """
    return db.insert("insert into spider_policy (company, name, depCode, arrCode, dateRange, spiderName, weeks) values "
                     "(%s, %s, %s, %s, %s, %s, %s)", company, name, depCode, arrCode, dateRange, spiderName, weeks)

# ======================================================================
# EXECL相关
# ======================================================================


def get_detail_task(company):
    """
    根据航司获取flight_detail表中的数据
    :return:
    """
    # if company == "JR":
    #     return db.query('select * from flight_detail_jr WHERE share=0 AND company=%s', company)
    # else:
    #     return db.query('select * from flight_detail WHERE share=0 AND company=%s', company)
    return db.query('select * from flight_detail WHERE share=0 AND company=%s', company)


def get_base_data(flightno, depcode, arrcode, company, week=""):
    """
    获取**_flight_base中的数据
    :return:
    """
    table_name = '%s_flight_base' % company.lower()
    if week == "":
        return db.get('select planTime from %s WHERE flightNo="%s" AND depcode="%s" AND arrcode="%s" AND '
                      'company="%s"' % (table_name, flightno, depcode, arrcode, company))
    else:
        return db.get('select planTime from %s WHERE flightNo="%s" AND depcode="%s" AND arrcode="%s" AND '
                      'company="%s" AND  week="%s"' % (table_name, flightno, depcode, arrcode, company, week))


def get_cabin_change(cabin, company):
    return db.get('select * FROM flight_cabin_change WHERE cabin=%s AND company=%s', cabin, company)


# ======================================================================
# 代理相关
# ======================================================================


def insert_http_prxoy(remoteId, proxyUrl, state=0):
    """
    添加代理
    :param remoteId:
    :param proxyUrl:
    :param state:
    :return:
    """
    sql = "insert into http_proxy (remoteId, proxyUrl, state) values (%s, %s, %s)"
    return db.insert(sql, int(remoteId), proxyUrl, state)


def insert_http_prxoy_history(hpid, website):
    """
    添加代理历史记录
    :param hpid:
    :param website:
    :return:
    """
    sql = "insert into http_proxy_history (hpid, website) values (%s, %s)"
    return db.insert(sql, hpid, website)


def update_http_prxoy_history(hpid):
    """
    更新代理使用历史
    :param hpid:
    :return:
    """
    db.update("UPDATE http_proxy_history SET endTime=NOW() WHERE hpid=%s and endTime is NULL", hpid)


def get_unused_http_prxoy(hpid=-1, user="", max_proxy=0):
    """
    查询当前可用的代理
    :param hpid:
    :return:
    """
    if hpid == -1:
        rst = db.get("SELECT count(id) as count FROM http_proxy WHERE state=1 AND `user`=%s", user)
        if rst["count"] < max_proxy:
            http_proxys = db.query("SELECT * FROM http_proxy WHERE state in (0, 2) limit 50")
            while http_proxys:
                http_proxy = random.choice(http_proxys)
                rowcount = db.execute_rowcount(
                    "UPDATE http_proxy SET state=1, `user`=%s WHERE id=%s", user, http_proxy['id'])
                if rowcount > 0:
                    return http_proxy
        return None
    else:
        return db.get("SELECT * FROM http_proxy WHERE id=%s" % hpid)


def update_http_prxoy_state(hid, new_state, old_state):
    """
    更新代理使用状态
    :param hid:
    :param state: default 0, 0未使用,1使用中,2使用完成,3废弃
    :return:
    """
    sql = "UPDATE http_proxy SET state=%s WHERE state in (%s) AND id=%s" % (new_state, old_state, hid)
    return db.update(sql)


def update_all_http_prxoy_state():
    """
    更新所有代理使用状态
    :param state: default 0, 0未使用,1使用中,2使用完成,3废弃
    :return:
    """
    return db.update("UPDATE http_proxy SET state=3 WHERE 1")


def get_discard_http_prxoy():
    """
    查询所有未过期的代理
    :return:
    """
    return db.query("SELECT * FROM http_proxy WHERE state <> 3")


def count_http_prxoy(start_time, end_time):
    """
    统计一次代理使用
    :param start_time:
    :param end_time:
    :return:
    """
    return db.get("SELECT count(id) as `count` FROM http_proxy WHERE %s < createTime and createTime < %s", start_time,
                  end_time)


def get_sys_config(ctype, cname="", status=1):
    """
    查询配置信息
    :return:
    """
    if cname:
        return db.get("SELECT * FROM sys_config WHERE cname=%s AND ctype=%s and status=%s ORDER BY createTime DESC",
                      cname, ctype, status)
    else:
        return db.query("SELECT * FROM sys_config WHERE ctype=%s and status=%s ORDER BY createTime DESC",
                      ctype, status)

