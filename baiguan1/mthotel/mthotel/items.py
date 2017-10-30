# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MthotelItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    detail = scrapy.Field()

    def __repr__(self):
        return '=================detail success==============' 
