#!/usr/bin/python
# -*-coding:utf-8-*-
__author__ = 'fly'

import sys
import time
import logging
import subprocess
from datetime import datetime

import pika

from flightspider import database
from flightspider import settings
from flightspider.lib import http_proxy
from flightspider.create_execl import create_xls
from flightspider.create_execl import create_prepay_xls

reload(logging)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='%s/log/spider.log' % settings.PROJECT_DIR,
                    filemode='a')

COMPANY_DICT = {"CA": "国航",
                "CZ": "南航",
                "MU": "东航",
                "EU": "成都航空",
                "G5": "华夏航空",
                "JR": "幸福航空",
                "MF": "厦门航空",
                "TV": "西藏航空",
                "FU": "福州航空",
                "NS": "河北航空",
                "9H": "长安航空",
                "BK":"奥凯航空",
                }


def manager(company, limit):
    try:
        commands = 'ps -ef|grep "taskmanager.py %s"|grep -v "grep" -c' % company
        p = subprocess.Popen(commands, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        check_proc = p.stdout.read()
        if int(check_proc.strip()) > 1:
            print '+++++++++' + check_proc + '-----------'
            logging.warn("前一次任务还在执行，本次任务退出... %s", check_proc)
            return
    except:
        pass

    limit = int(limit)
    offset = 0
    start_time = time.time()
    logging.info("初始化抓取策略状态...")
    database.reset_spider_policy(company=company)
    sys_proxy = database.get_sys_config(2, cname=company)
    proxys = 0
    if sys_proxy:
        proxys += int(sys_proxy["cvalue"])
        if proxys:
            logging.info("准备代理中...")
            http_proxy_count = http_proxy.btach_replace_http_proxy(proxys)
            logging.info("成功请求代理数量：%s" % http_proxy_count)
        logging.info("开始分发任务...")

    if check_message(company):
        print check_message(company),11
     # send_mail("%s可能官网较慢，消息队列存在未完成消息。请排查。" % company)
        logging.info("%s可能官网较慢，消息队列存在未完成消息。请排查。已发送邮件" % company)
        return
    while True:
        rst = database.get_all_tasks(offset, limit, company=company)
        if not rst:
            break
        offset += limit
        for item in rst:
            database.update_task_state(int(item["id"]), 1)
            push_message(str(item), company)
        # 针对FU等需要一次运行全部策略的情况
        if limit == 1:
            break
    logging.info("完成任务初次分发 ^_^ ")
    monitor_task(company)
    done_time = time.time()
    run_time = int((done_time - start_time) / 60)
    spider_count = {}
    if company:
        for cy in company.split(","):
            spider_count[COMPANY_DICT.get(cy)] = int(database.count_spider_flight(cy)["count"])
    else:
        companys = database.get_enabled_company()
        for cy in companys:
            spider_count[COMPANY_DICT.get(cy)] = int(database.count_spider_flight(cy)["count"])

    http_proxy_count = database.count_http_prxoy(datetime.fromtimestamp(start_time), datetime.fromtimestamp(done_time))[
        "count"]
    logging.info("本次抓取耗时:%s分钟" % run_time)
    for k, v in spider_count.iteritems():
        logging.info("%s:%s" % (k, v))

    logging.info("代理使用:%s" % http_proxy_count)
    logging.info("=" * 30)
    # 生成execl
    # publish_xls(company)


def monitor_task(company):
    """获取剩余任务数量"""
    fix_times = 0
    while True:
        count = get_message_count(company)
        if count == 0:
            count_error = database.count_task_by_work_state(4, company)["count"]
            if count_error == 0:
                logging.info("爬取数据完成 ^_^ ")
                return
            http_proxy_count = http_proxy.btach_replace_http_proxy(17)
            logging.info("成功请求代理数量：%s" % http_proxy_count)
            fix_times += 1
            if fix_times > 2:
                logging.info("%d次尝试重试未完成的任务数量为：%s,请检查日志" % (fix_times, count_error))
                return
            offset = 0
            limit = 30
            while True:
                rst = database.get_task_by_work_state(4, offset, limit, company)
                offset += limit
                if not rst:
                    break
                for item in rst:
                    database.update_task_state(int(item["id"]), 1)
                    push_message(str(item), company)
            logging.info("重新爬取未完成的任务%d次 @@" % fix_times)
        time.sleep(60)



def get_message_count(company):
    credentials = pika.PlainCredentials(settings.APP_USER, settings.APP_PASS)
    if settings.TEST_ENVIRONMENT:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=settings.RABBITMQ_SERVER_TEST, credentials=credentials))
    else:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=settings.RABBITMQ_SERVER, credentials=credentials))
    channel = connection.channel()
    if company:
        q = channel.queue_declare('flight_%s' % company.replace(",", "_").lower(), durable=True)
    else:
        q = channel.queue_declare('flight', durable=True)

    #str_rabbitmq_count = subprocess.check_output(["rabbitmqctl", "list_queues"])
    #lists = str_rabbitmq_count.split('\n')
    #if company:
    #    sel_flight = 'flight_%s' % company.replace(",", "_").lower()
    #else:
    #    sel_flight = 'flight'
    #for var in lists:
    #    if var.find(sel_flight) != -1:
    #        var_list = var.split('\t')
    #        return int(var_list[1])

    return q.method.message_count


def push_message(msg, company):
    if company:
        queue_key = 'flight_%s' % company.replace(",", "_").lower()
    else:
        queue_key = 'flight'
    credentials = pika.PlainCredentials(settings.APP_USER, settings.APP_PASS)
    if settings.TEST_ENVIRONMENT:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=settings.RABBITMQ_SERVER_TEST, credentials=credentials))
    else:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=settings.RABBITMQ_SERVER, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue=queue_key, durable=True)
    channel.basic_qos(prefetch_count=1)
    message = msg
    channel.basic_publish(exchange=settings.EXCHANGE_DARKMATTER,
                          routing_key=queue_key,
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          ))
    connection.close()


def publish_xls(company):
    company_list = company.split(',')
    for cy in company_list:
        create_xls.cy_xls(cy)
        create_prepay_xls.cy_xls(cy)


def check_message(company):
    if company:
        queue_key = 'flight_%s' % company.replace(",", "_").lower()
    else:
        queue_key = 'flight'
    credentials = pika.PlainCredentials(settings.APP_USER, settings.APP_PASS)
    if settings.TEST_ENVIRONMENT:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=settings.RABBITMQ_SERVER_TEST, credentials=credentials))
    else:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=settings.RABBITMQ_SERVER, credentials=credentials))
    channel = connection.channel()
    q = channel.queue_declare(queue=queue_key, durable=True)
        # channel.basic_qos(prefetch_count=1)
    try:
        count = q.method.message_count  # + channel.get_waiting_message_count()
        print count
        connection.close()
    except Exception as e:
        print e

    if count:
       return True
                                                                                                                                        # 查看队列剩余消息数

if __name__ == "__main__":
    company = None
    limit = 30
    if len(sys.argv[1:]) > 0:
        company = sys.argv[1]
        try:
            limit_tmp = sys.argv[2]
            limit = limit_tmp
        except:
            pass
    if company:
        for item in company.split(","):
            if item not in COMPANY_DICT.keys():
                print "%s 参数错误!"
                sys.exit()
    manager(company, limit)
