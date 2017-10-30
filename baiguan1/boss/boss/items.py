# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BossItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    detail = scrapy.Field()

    def __repr__(self):
        return '=================BossItemdetail success=============='

class BossCompanyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    detail = scrapy.Field()

    def __repr__(self):
        return '=================BossCompanyItem success=============='

class BossniuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    detail = scrapy.Field()

    def __repr__(self):
        return '=================BossniuItem success=============='