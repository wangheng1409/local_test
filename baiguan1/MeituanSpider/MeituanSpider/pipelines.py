# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from MeituanSpider.items import MeituanspiderItem, MenuItem, WebPoiItem, WebMenuItem
from MeituanSpider.items import WapPoiItem, WapMenuItem
import json
from MeituanSpider.util.RedisQueue import RedisQueue


class MeituanspiderPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(settings['MONGODB_URI'])
        # self.client = pymongo.MongoClient()
        self.db = self.client[settings['MONGODB_DB']]
        self.poi_handler = None
        self.menu_handler = None
        self.web_poi_handler = None
        self.web_menu_handler = None
        self.wap_poi_handler = None
        self.wap_menu_handler = None
        self.wap_menu_list = []
        self.redis_client = RedisQueue()
        self.writer = open('menu.txt_redis_lost_2', 'a', encoding='utf-8')

    def process_item(self, item, spider):
        if isinstance(item, MeituanspiderItem):
            self.process_poi(item)
        elif isinstance(item, MenuItem):
            self.process_menu(item)
        elif isinstance(item, WebPoiItem):
            self.process_web_poi(item)
        elif isinstance(item, WebMenuItem):
            self.process_web_menu(item)
        elif isinstance(item, WapPoiItem):
            self.process_wap_poi(item)
        elif isinstance(item, WapMenuItem):
            self.process_wap_menu(item)
        return item

    def process_poi(self, item):
        if not self.poi_handler:
            self.poi_handler = self.db[settings['MONGODB_POI_COLLECTION']]
        poi_dict = item['poi_item']
        poi_id = poi_dict['id']
        existed = self.redis_client.sput('poi_id', poi_id)
        if 1 == existed:
            self.poi_handler.insert(poi_dict)

    def process_menu(self, item):
        if not self.menu_handler:
            self.menu_handler = self.db[settings['MONGODB_MENU_COLLECTION']]
        dict_from_json = item['dict_from_json']
        self.writer.write(json.dumps(dict_from_json))
        self.writer.write('\n*************\n')
        # self.menu_handler.insert(dict_from_json)

    def process_web_poi(self, item):
        if not self.web_poi_handler:
            self.web_poi_handler = self.db[settings['MONGODB_WEB_POI_COLLECTION']]
        list_dict_from_json = item['list_dict_from_json']
        self.web_poi_handler.insert_many(list_dict_from_json)

    def process_web_menu(self, item):
        if not self.web_menu_handler:
            self.web_menu_handler = self.db[settings['MONGODB_WEB_MENU_COLLECTION']]
        self.web_menu_handler.insert(dict(item))

    def process_wap_poi(self, item):
        if not self.wap_poi_handler:
            self.wap_poi_handler = self.db[settings['MONGODB_WAP_POI_COLLECTION']]
        self.wap_poi_handler.insert(dict(item))

    def process_wap_menu(self, item):
        if not self.wap_menu_handler:
            self.wap_menu_handler = self.db[settings['MONGODB_WAP_MENU_COLLECTION']]
        self.wap_menu_list.extend(item['list_dict_from_json'])
        if len(self.wap_menu_list) >= 10000:
            self.wap_menu_handler.insert(self.wap_menu_list)
            self.wap_menu_list = []

    def close_spider(self, spider):
        if self.wap_menu_list:
            self.wap_menu_handler.insert(self.wap_menu_list)
        self.client.close()
        self.writer.close()
