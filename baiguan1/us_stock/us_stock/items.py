# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class UsStockItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # filer = scrapy.Field()
    # shares_held = scrapy.Field()
    # market_value = scrapy.Field()
    # percent_of_portfolio = scrapy.Field()
    # prior_of_portfolio = scrapy.Field()
    # ranking = scrapy.Field()
    # change_in_shares = scrapy.Field()
    # ownership = scrapy.Field()
    # source = scrapy.Field()
    # source_date = scrapy.Field()
    # ts_string = scrapy.Field()
    # ts = scrapy.Field()
    detail = scrapy.Field()
    def __repr__(self):
        return '=================%s     success==============' %(self.name)
