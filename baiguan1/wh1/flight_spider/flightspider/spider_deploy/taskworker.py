# -*-coding:utf-8-*-
__author__ = 'fly'
'''
爬虫执行逻辑
'''

import os
import sys
import time
import pika
import flightspider.settings
import logging
from flightspider import settings

def callback(ch, method, properties, body,ipindex):
    task = eval(body)
    print settings.PROJECT_DIR
    os.system("cd %s" % settings.PROJECT_DIR)
    if ipindex :
        cmd = "scrapy crawl %s -a task_id=%s  -a ipindex=%s" % (task["spiderName"], task["id"],ipindex)
    else:
        cmd = "scrapy crawl %s -a task_id=%s -L DEBUG" % (task["spiderName"], task["id"])
    logging.info(cmd)
    os.system(cmd)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def consume(companys,ipindex=None):

    """
    监听rabbitmq 消息队列执行爬虫任务
    :param companys:
    :return:
    """
    main_queue_key = companys[0].replace(",", "_").lower()
    credentials = pika.PlainCredentials(flightspider.settings.APP_USER, flightspider.settings.APP_PASS)
    if flightspider.settings.TEST_ENVIRONMENT:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=flightspider.settings.RABBITMQ_SERVER_TEST, credentials=credentials))
    else:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=flightspider.settings.RABBITMQ_SERVER, credentials=credentials))
    channel = connection.channel()
    while 1:
        for company in companys:
            queue_key = company.replace(",", "_").lower()
            channel.basic_qos(prefetch_count=1)
            q = channel.queue_declare(main_queue_key, durable=True)
            if q.method.message_count > 0:
                queue_key = main_queue_key
            method, properties, body = channel.basic_get(queue=queue_key)
            if method:
                callback(channel, method, properties, body,ipindex)
        time.sleep(1)

if __name__ == '__main__':
    #参数1：flight_公司code
    # 参数2：代理索引 ipindex
    if len(sys.argv[1:]) == 2:
        consume([sys.argv[1]],sys.argv[2])
    elif len(sys.argv[1:]) == 1:
        consume([sys.argv[1]])
    else:
        print 'Unknown company pararm.'
        sys.exit()