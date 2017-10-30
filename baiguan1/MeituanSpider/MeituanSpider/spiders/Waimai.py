# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from scrapy.conf import settings
import random
import uuid
import time
import json
import datetime
from MeituanSpider.items import MeituanspiderItem


class WaimaiSpider(RedisSpider):
    name = "Waimai"
    allowed_domains = ["meituan.com"]
    start_urls = ['https://wx.waimai.meituan.com/weapp/v1/poi/filter']
    headers = settings['HEADERS']
    redis_key = 'Waimai'

    def make_request_from_data(self, data):
        latitude_offset = settings['LATITUDE_OFFSET']
        longitude_offset = settings['LONGITUDE_OFFSET']
        location = json.loads(data.decode())
        name = location['name']
        already = []
        if name not in already:
            already.append(name)
        if '单价' not in name and '总价' not in name and '佣金' not in name:
            latitude = float(location['lat'])
            longitude = float(location['lng'])
            if (38.66 < float(latitude) < 41.22) and (115.071 < float(longitude) < 117.687):
                poi_url = settings['POI_URL']
                param_template = settings['POI_DATA'].copy()
                param = param_template
                param['wm_actual_latitude'] = str(int(latitude * 1000000))
                param['wm_actual_longitude'] = str(int(longitude * 100000))
                param['wm_latitude'] = str(int(latitude * 1000000 + random.randint(-latitude_offset, latitude_offset)))
                param['wm_longitude'] = str(int(longitude * 1000000 + random.randint(-longitude_offset, longitude_offset)))
                param['req_time'] = str(int(time.time() * 1000))
                param['wm_uuid'] = str(uuid.uuid4())
                param['wm_visitid'] = str(uuid.uuid4())
                return scrapy.FormRequest(poi_url,
                                          formdata=param,
                                          headers=self.headers,
                                          meta={'param': param,
                                                'area_name': name,
                                                'latitude': str(latitude),
                                                'longitude': str(longitude),
                                                'action': 'visit_first_page'})

    def parse(self, response):
        area_name = response.meta['area_name']
        try:
            poi_data = json.loads(response.body.decode()).get('data', [])
        except Exception:
            return
        if not poi_data:
            return

        poi_list = poi_data['poilist']
        for poi in poi_list:
            item = MeituanspiderItem()
            poi['area_name'] = area_name
            poi['ts'] = str(datetime.datetime.fromtimestamp(time.time(), None))
            poi['ts_string'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            item['poi_item'] = poi
            yield item

        page_index = poi_data['page_index']
        if page_index == 1:
            total_page_num = poi_data['poi_total_num'] // 20 + 1
            for page in range(2, total_page_num + 1):
                param = response.meta['param']
                param['page_index'] = str(page)
                yield scrapy.FormRequest(response.url,
                                         callback=self.parse,
                                         formdata=param,
                                         headers=self.headers,
                                         meta={'param': param,
                                               'area_name': area_name,
                                               'action': 'visit_later_page'})
