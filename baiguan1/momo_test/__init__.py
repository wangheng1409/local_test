# coding=utf-8
import time
import datetime
import redis
import json
import re
import gc
import random
import sys
import copy
import threading
from pympler import summary
from pympler import muppy
from urllib import parse
from bo_lib.general import ProxyManager
from concurrent.futures import ThreadPoolExecutor, as_completed
import pymongo
from selenium import webdriver

from bo_lib.general.redis_helper import RedisHelper



client = pymongo.MongoClient('mongodb://root:Baiguan2016@60.205.152.167:3717')
collection = client.momo.momo_paying_user
pm = ProxyManager()
r = RedisHelper().client


class UserInfo:
    def __init__(self,id_list):
        # Chrome设置
        ChromeOptions = webdriver.ChromeOptions()
        # 设置参数
        ChromeOptions.add_argument('window-size=1200x600')  # 窗口大小。不可见，最好人工设置。
        ChromeOptions.add_argument("--disable-extensions")  # 不加载扩展。
        # ChromeOptions.add_argument("--headless")  # 开启无头模式。即使是无头模式，也会开启Chrome浏览器，只是不会显式执行具体操作。
        # ChromeOptions.add_argument('--proxy-server=http://123.59.69.66:8081')
        self.driver=webdriver.Chrome(chrome_options=ChromeOptions)
        self.id_list=id_list
        self.get_user_info_list(self.id_list,self.driver)
        self.driver.close()

    def get_user_info_list(self,id_list,driver):
        for id in id_list:
            try:
                # 构造url
                url = "https://api.immomo.com/live/{id}".format(id=id)
                # 加载网页
                driver.get(url)
                # 等待加载头像
                # time.sleep(3)
                driver.implicitly_wait(20)
                # 点击头像
                driver.find_element_by_xpath("//div[@class='anchorInfo']//*[@class='anchorIcon']").click()
                # 等待加载主播信息
                # time.sleep(3)
                driver.implicitly_wait(20)
                # 获取主播信息
                user_info = {}
                user_info['id']=id
                user_info['name'] = driver.find_element_by_xpath("//p[contains(@class, 'profileName')]").text
                user_info['sex'] = driver.find_element_by_xpath(
                    "//div[contains(@class,'profileContent')]//img[contains(@class, 'sexIcon')]").get_attribute('src')
                user_info['fortunelevel'] = driver.find_element_by_xpath(
                    "//div[contains(@class,'profileContent')]//img[contains(@class, 'fortunelevel level level')]").get_attribute(
                    'data-fortune')
                user_info['charmlevel'] = driver.find_element_by_xpath(
                    "//div[contains(@class,'profileContent')]//img[contains(@class, 'charmlevel level level')]").get_attribute(
                    'data-charm')
                print(user_info)
                collection.insert(user_info,check_keys=False)
            except Exception as e:
                print('--- error: {e}'.format(e=e))


def cut_list(old_list, _slice=10):
    new_list = []  # 切成功后的 ：[[],[],[],[]]
    for i in range(len(old_list) // _slice):
        a = old_list[:_slice]
        del old_list[:_slice]
        new_list.append(a)
    len_new_list = len(new_list) * 1000
    print('new_list ok', len_new_list)
    return new_list, len_new_list

def gen_executor(work, slice_list):
    workers = 5
    with ThreadPoolExecutor(workers) as executor:
        futures = [executor.submit(work, slice_item) for slice_item in slice_list]
        for future in as_completed(futures):
            futures.remove(future)
            yield

if __name__ == '__main__':
    # for i in range(1000):
    #     # res = random.choice(['1', '2', '3', '4']) + "%0.8d" % random.randint(0, 99999999)
    #     res = random.choice(['47',]) + "%0.7d" % random.randint(0, 9999999)
    #     r.sadd('momo_paying_user_0',json.dumps(res))
    # redis_id_list=[json.loads(x) for x in r.smembers('momo_paying_user_0')]
    redis_id_list=[
        '554829477',
        # '398589368',
        # '430350771',
        # '101003663',
    ]
    obj=UserInfo(redis_id_list)