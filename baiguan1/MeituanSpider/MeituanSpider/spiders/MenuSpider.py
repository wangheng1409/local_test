# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from scrapy.conf import settings
import random
import uuid
import time
import json
from MeituanSpider.items import MenuItem
import redis
from scrapy.conf import settings


class MenuspiderSpider(RedisSpider):
    name = "MenuSpider"
    allowed_domains = ["meituan.com"]
    start_urls = ['http://meituan.com/']
    headers = settings['HEADERS']
    #settings['REDIS_START_URLS_AS_SET'] = True
    #menu_handler = MongoUtil('Menu').handler
    redis_key = 'MenuSpider'
    pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db='0', password='bigone2016')
    r = redis.Redis(connection_pool=pool)

    def make_request_from_data(self, data):
        menu_url = settings['MENU_URL']
        poi = json.loads(data.decode(), encoding='utf-8')
        param = self.generate_param(poi)
        return scrapy.FormRequest(menu_url,
                                  formdata=param,
                                  headers=self.headers,
                                  meta={'id': poi['id'],
                                        'longitude': poi['longitude'],
                                        'latitude': poi['latitude']})

    def parse(self, response):
        poi_id = response.meta['id']
        latitude = response.meta['latitude']
        longitude = response.meta['longitude']
        menu_json = response.body.decode()
        try:
            data_dict = json.loads(menu_json).get('data', {})
        except Exception:
            self.retry_this_poi({'id': int(poi_id),
                                 'latitude': latitude,
                                 'longitude': longitude})
            return

        if not isinstance(data_dict, dict):
            self.retry_this_poi({'id': int(poi_id),
                                 'latitude': latitude,
                                 'longitude': longitude})
            return

        spu_list = data_dict.get('food_spu_tags', [])
        if not spu_list:
            self.retry_this_poi({'id': int(poi_id), 'latitude': latitude, 'longitude': longitude})
        for spu in spu_list:
            spus_list = spu.get('spus', [])
            for spus in spus_list:
                spus['poi_id'] = poi_id
                item = MenuItem()
                item['dict_from_json'] = spus
                yield item

    def retry_this_poi(self, param):
        self.r.sadd('MenuSpider', json.dumps(param))

    def random_sentence(self, num):
        s = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
        s_list = [x for x in s]
        random.shuffle(s_list)
        result = ''.join(s_list[:num])
        return result

    def token(self):
        return '{}_{}-{}-{}_{}'.format(self.random_sentence(13),
                                       self.random_sentence(10),
                                       self.random_sentence(39),
                                       self.random_sentence(17),
                                       self.random_sentence(19))

    def random_id(self):
        return random.randint(3761112, 3781112)

    def generate_param(self, poi):
        param = settings['MENU_DATA'].copy()

        latitude_offset = settings['LATITUDE_OFFSET']
        longitude_offset = settings['LONGITUDE_OFFSET']
        longitude = poi['longitude'] + random.randint(-longitude_offset, longitude_offset)
        latitude = poi['latitude'] + random.randint(-latitude_offset, latitude_offset)
        param['wm_poi_id'] = str(poi['id'])
        param['req_time'] = str(int(time.time() * 1000))
        param['wm_uuid'] = str(uuid.uuid4())
        param['wm_visitid'] = str(uuid.uuid4())
        tok = self.token()
        param['userToken'] = tok
        param['wm_logintoken'] = tok
        user_id = self.random_id()
        param['user_id'] = str(user_id)
        param['userid'] = str(user_id)
        param['wm_actual_latitude'] = str(latitude)
        param['wm_actual_longitude'] = str(longitude)
        param['wm_latitude'] = str(latitude + random.randint(-latitude_offset, latitude_offset))
        param['wm_longitude'] = str(longitude + random.randint(-longitude_offset, longitude_offset))
        return param

