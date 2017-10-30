# -*- coding: utf-8 -*-
import scrapy
import random
from urllib.parse import quote
from selenium import webdriver
from scrapy.conf import settings
import json
import datetime
import time

from MeituanSpider.util.util import query_location


class PoiwapSpider(scrapy.Spider):
    name = "PoiWap"
    # allowed_domains = ["i.waimai.meituan.com"]
    start_urls = ['http://i.waimai.meituan.com/']
    wap_url = settings['WAP_URL']
    wap_poi_url = settings['WAP_POI_URL']
    driver = webdriver.PhantomJS('./phantomjs')
    with open('meituan.js') as f:
        js = f.read()

    def start_requests(self):
        # location_list = query_location()
        location_list = [{'latitude': 39.950516, 'longitude': 116.420155, 'name': '雍和家园'}]
        for location in location_list:
            latitude = location['latitude']
            longitude = location['longitude']
            url = self.wap_url.format(lat=latitude, lng=longitude)
            yield scrapy.Request(url,
                                 headers=settings['WAP_HEADERS'],
                                 meta={'location': location})

    def parse(self, response):
        location = response.meta['location']
        headers = settings['WAP_POI_HEADER'].copy()
        cookies = response.headers.getlist('Set-Cookie')
        poi_cookies = [x.decode() for x in cookies]
        poi_cookies_str = self.generate_cookies(poi_cookies, location)
        headers['Cookie'] = poi_cookies_str
        data = settings['WAP_POI_DATA']
        url = self.wap_poi_url.format(token=self.generate_token(data))
        yield scrapy.FormRequest(url,
                                 callback=self.parse_poi,
                                 headers=headers,
                                 formdata=data,
                                 meta={'formdata': data,
                                       'headers': headers,
                                       'location': location})

    def parse_poi(self, response):
        location = response.meta['location']
        formdata = response.meta['formdata'].copy()
        headers = response.meta['headers']
        poi_info_json = response.body.decode()
        try:
            poi_info_dict = json.loads(poi_info_json)
        except Exception:
            print('poi info json is invalid.')
            return
        poi_data = poi_info_dict.get('data', {})
        if not poi_data:
            print('poi data is empty.')
            return
        page_index = poi_data.get('page_index', -1)
        poi_has_next_page = poi_data.get('poi_has_next_page', False)
        poi_list = poi_data.get('poilist', [])
        for poi in poi_list:
            poi['area_name'] = location['name']
            poi['ts'] = datetime.datetime.fromtimestamp(time.time(), None)
            poi['ts_string'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            item = WapPoiItem()
            item['dict_from_json'] = poi
            yield item

        if poi_has_next_page:
            formdata['page_index'] = page_index + 1
            url = settings['WAP_POI_URL'].format(token=self.generate_token(formdata))
            yield scrapy.FormRequest(url,
                                     callback=self.parse_poi,
                                     headers=headers,
                                     formdata=formdata,
                                     meta={'formdata': formdata,
                                           'headers': headers,
                                           'location': location})

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
