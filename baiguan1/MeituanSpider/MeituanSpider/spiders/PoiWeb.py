# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from scrapy.conf import settings
from selenium import webdriver
from selenium.webdriver.remote.remote_connection import LOGGER

import random
import json
import datetime
import time
import logging
import re
import random
from MeituanSpider.items import WebPoiItem, WebMenuItem
from MeituanSpider.util.MongoUtil import MongoUtil


LOGGER.setLevel(logging.INFO)


class PoiwebSpider(RedisSpider):
    name = "PoiWeb"
    redis_key = 'PoiWeb:start_urls'
    allowed_domains = ["meituan.com"]
    poi_headers = settings['WEB_POI_HEADER']
    poi_url = settings['WEB_POI_URL']
    poi_param = settings['WEB_POI_DATA']
    driver = webdriver.PhantomJS('./phantomjs')
    with open('meituan.js') as f:
        js = f.read()

    def start_requests(self):
        handler = MongoUtil('lng-lat').handler
        location_list = [x for x in handler.find({}, {'_id': 0})]
        random.shuffle(location_list)
        already = []
        for location in location_list:
            name = location['name']
            if name in already:
                continue
            already.append(name)
            if '单价' in name or '总价' in name or '佣金' in name:
                continue
            latitude = location['lat']
            longitude = location['lng']
            if not ((38.66 < float(latitude) < 41.22) and (115.071 < float(longitude) < 117.687)):
                print('Skip-->: {}, {}, {}'.format(name, latitude, longitude))
                continue
            headers = settings['WEB_GEOID_HEADERS'].copy()
            headers['Cookie'].format(latitude=latitude, longitude=longitude, name=name)
            url = settings['WEB_POI_SEARCH_URL'].format(name=name, latitude=latitude, longitude=longitude)
            yield scrapy.Request(url, headers=headers, meta={'area_name': name})

    # def make_request_from_data(self, data):
    #     """
    #     Override RedisSpider's inner method. So a requests with special headers can be sent.
    #
    #     :param data: it is the url readed from redis. it is a bytes data.
    #     :return:
    #     """
    #     url = data.decode()
    #     name = re.search('addr=(.*?)\&', url).group(1)
    #     latitude = re.search('lat=(.*?)\&', url).group(1)
    #     longitude = re.search('lng=(.*?)\&', url).group(1)
    #     if not ((38.66 < float(latitude) < 41.22) and (115.071 < float(longitude) < 117.687)):
    #         return
    #     headers = settings['WEB_GEOID_HEADERS'].copy()
    #     headers['Cookie'].format(latitude=latitude, longitude=longitude, name=name)
    #     return scrapy.Request(url, headers=headers, meta={'area_name': name})

    def parse(self, response):
        area_name = response.meta['area_name']
        cookies = response.headers.getlist('Set-Cookie')
        poi_cookies = [x.decode() for x in cookies]
        poi_cookies_str = self.generate_cookies(poi_cookies)
        headers = self.poi_headers.copy()
        headers['Cookie'] = poi_cookies_str
        headers['Referer'] = response.url
        friendly_token_dict = self.poi_param.copy()
        unfriendly_token_str = self.generate_token(friendly_token_dict)
        poi_url = self.poi_url.format(unfriendly_token_str)

        yield scrapy.FormRequest(poi_url,
                                 callback=self.parse_poi,
                                 formdata=friendly_token_dict,
                                 headers=headers,
                                 meta={'friendly_token_dict': friendly_token_dict,
                                       'poi_headers': headers,
                                       'area_name': area_name})

    def parse_poi(self, response):
        area_name = response.meta['area_name']
        friendly_token_dict = response.meta['friendly_token_dict'].copy()
        headers = response.meta['poi_headers']
        try:
            data = json.loads(response.body.decode())['data']
        except Exception:
            print(response.body.decode())
            return

        poi_list = []
        for index, poi in enumerate(data['poiList']):
            wm_poi_web = poi['wmPoi4Web']
            wm_poi_web['ts'] = datetime.datetime.fromtimestamp(time.time(), None)
            wm_poi_web['area_name'] = area_name
            poi_list.append(wm_poi_web)

            poi_id = wm_poi_web['wm_poi_id']
            pos = index % 20 # range of pos is 0~19

            # menu_url = settings['WEB_MENU_URL'].format(poi_id, pos)
            # yield scrapy.Request(menu_url, callback=self.parse_menu, headers=headers, meta={'poi_id': poi_id})

        if poi_list:
            item = WebPoiItem()
            item['list_dict_from_json'] = poi_list
            yield item

        if data['hasMore']:
            friendly_token_dict['page_offset'] = str(int(friendly_token_dict['page_offset']) + 20)
            next_unfriendly_token_str = self.generate_token(friendly_token_dict)
            poi_url = self.poi_url.format(next_unfriendly_token_str)

            yield scrapy.FormRequest(poi_url,
                                     callback=self.parse_poi,
                                     formdata=friendly_token_dict,
                                     headers=headers,
                                     meta={'friendly_token_dict': friendly_token_dict,
                                           'poi_headers': headers,
                                           'area_name': area_name})

    def parse_menu(self, response):
        poi_id = response.meta['poi_id']
        menu_list = response.xpath('//div[starts-with(@class, "j-pic-food")]')
        for menu in menu_list:
            item = WebMenuItem()
            item['poi_id'] = poi_id
            item['name'] = menu.xpath('div[@class="np clearfix"]/span/@title').extract()[0]
            month_sale = menu.xpath('*/div[@class="sold-count ct-lightgrey"]/span/text()').extract()
            item['month_sale'] = month_sale[0] if month_sale else ''
            zan = menu.xpath('div[@class="sale-info clearfix"]/div[@class="fr zan-count"]/span[@class="cc-lightred-new"]/text()').extract()
            item['zan'] = zan[0] if zan else ''
            price = menu.xpath('*/div[@class="price fl"]/div/text()').extract()
            item['price'] = price[0] if price else ''
            item['ts'] = datetime.datetime.fromtimestamp(time.time(), None)
            yield item

    def generate_token(self, friendly_token_dict):
        friendly_token_str = '&'.join(['{}={}'.format(key, value) for key, value in friendly_token_dict.items()])
        unfriendly_token = self.driver.execute_script(self.js.replace('$token$', friendly_token_str))
        return unfriendly_token

    def random_sentence(self, num):
        s = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
        s_list = [x for x in s]
        random.shuffle(s_list)
        result = ''.join(s_list[:num])
        return result

    def generate_cookies(self, poi_cookies):
        poi_cookies.append('w_uuid={}-{}'.format(self.random_sentence(53), self.random_sentence(10)))
        poi_cookies.append('uuid=cf3116fa2cc8e00399d3.1490103155.0.0.0')
        poi_cookies.append('_ga=GA1.3.1482810645.1490103092')
        poi_cookies.append('__mta=46549400.1490103092603.1490446169753.1490446197804.4')
        return '; '.join(poi_cookies)
