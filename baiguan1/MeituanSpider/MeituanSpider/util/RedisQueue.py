import redis
import json
import time
from scrapy.conf import settings


class RedisQueue(object):
    def __init__(self):
        self.client = None
        self.connect()

    def connect(self):
        host = settings['REDIS_HOST']
        port = settings['REDIS_PORT']
        password = settings['REDIS_PASSWORD']
        self.client = redis.StrictRedis(host=host, port=port, password=password)

    def put(self, key, host):
        self.client.lpush(key, json.dumps(host).encode("utf-8"))

    def sput(self, key, data):
        return self.client.sadd(key, data)

    def get(self, wait=False):
        host = self.client.lpop(self.key)
        while wait and not host:
            time.sleep(1)
            host = self.client.lpop(self.key)
        host = host.decode()
        return json.loads(host) if host else {}
