import pymongo
from scrapy.conf import settings


class MongoUtil(object):
    def __init__(self, collection_name):
        self.collection_name = collection_name
        self._handler = None
        self.connect()

    def connect(self):
        client = pymongo.MongoClient(settings['MONGODB_URI'])
        db = client[settings['MONGODB_DB']]
        self._handler = db[self.collection_name]

    @property
    def handler(self):
        return self._handler
