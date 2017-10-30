# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class MeituanspiderItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    poi_item = Field()

    def __repr__(self):
        return '=================POI stored=============='


class MenuItem(Item):
    dict_from_json = Field()

    def __repr__(self):
        return '=================Menu stored=============='


class WebPoiItem(Item):
    list_dict_from_json = Field()

    def __repr__(self):
        return '=================POI stored=============='


class WapMenuItem(Item):
    list_dict_from_json = Field()

    def __repr__(self):
        return '=================POI stored=============='


class WapPoiItem(Item):
    dict_from_json = Field()

    def __repr__(self):
        return '=================POI stored=============='


class WebMenuItem(Item):
    poi_id = Field()
    name = Field()
    price = Field()
    zan = Field()
    month_sale = Field()
    ts = Field()

    def __repr__(self):
        return '=================Menu stored=============='
