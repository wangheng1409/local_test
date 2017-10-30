# -*- coding: utf-8 -*-
import scrapy
import random
from scrapy.conf import settings
from MeituanSpider.util.MongoUtil import MongoUtil
from urllib.parse import quote
from selenium import webdriver
import json
from MeituanSpider.items import WapMenuItem

class WapmenuSpider(scrapy.Spider):
    name = "WapMenu"
    allowed_domains = ["i.waimai.meituan.com"]
    start_urls = ['http://i.waimai.meituan.com/']
    wap_menu_url = settings['WAP_MENU_URL']
    wap_menu_post_url = settings['WAP_MENU_POST_URL']
    menu_handler = MongoUtil('Menu').handler
    driver = webdriver.PhantomJS('./phantomjs')
    with open('meituan.js', encoding='utf-8') as f:
        js = f.read()

    def start_requests(self):
        # crawled_poi = self.menu_handler.distinct('poi_id')
        # poi_handler = MongoUtil('WAP_POI').handler
        # poi_id_list = poi_handler.distinct('wm_poi_view_id')
        poi_id_list = ['72819363509169655']
        for poi_id in poi_id_list:
            # if poi_id in crawled_poi:
            #     print('==============crawled, skip===============')
            #     continue
            # crawled_poi.append(poi_id)
            location = {'name': '雍和家园'}
            url = self.wap_menu_url.format(poi_id)
            yield scrapy.Request(url,
                                 headers=settings['WAP_HEADERS'],
                                 meta={'poi_id': poi_id,
                                       'location': location,
                                       'headers': settings['WAP_POI_HEADER'].copy()})

    def parse(self, response):
        poi_id = response.meta['poi_id']
        location = response.meta['location']
        headers = response.meta['headers']
        cookies = response.headers.getlist('Set-Cookie')
        poi_cookies = [x.decode() for x in cookies]
        poi_cookies_str = self.generate_cookies(poi_cookies, location)
        headers['Cookie'] = poi_cookies_str
        form_data = {'wm_poi_id': poi_id}
        token = self.generate_token(form_data)
        menu_post_url = self.wap_menu_post_url.format(token)
        yield scrapy.FormRequest(menu_post_url,
                                 callback=self.parse_menu,
                                 formdata=form_data,
                                 headers=headers)

    def parse_menu(self, response):
        menu_json = response.body.decode()
        try:
            menu_dict = json.loads(menu_json)
        except Exception:
            return
        menu_data = menu_dict.get('data', {})
        food_spu_tags = menu_data.get('food_spu_tags', [])
        for spu_tag in food_spu_tags:
            spu_list = spu_tag['spus']
            item = WapMenuItem()
            item['list_dict_from_json'] = spu_list
            yield item

    def generate_cookies(self, poi_cookies, location):
        poi_cookies = [x.split(';')[0] for x in poi_cookies]
        skip_list = ['lt=', 'n=', 'SID=', 'isid=']
        poi_cookies = [x for x in poi_cookies if x not in skip_list]
        poi_cookies.append('_ga=GA1.2.2129559026.1490150745; _ga=GA1.3.2129559026.1490150745')
        poi_cookies.append('__mta=155426692.1490150744886.1490955901717.1491367358316.51')
        poi_cookies.append('__mta=155426692.1490150744886.1491367358316.1491383119417.52')
        poi_cookies.append('wx_channel_id=0')
        poi_cookies.append('_lx_utm=')
        poi_cookies.append('_lxsdk_s=3ca837a42930b064a14dc11d6440%7C%7C4')
        poi_cookies.append('w_addr={}'.format(quote(location['name'])))
        poi_cookies.append('webp=1; _lxsdk=15b3c97f8c2c8-0a880f0d3dbcb-1d3c6853-384000-15b3c97f8c231')
        return '; '.join(poi_cookies)

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
