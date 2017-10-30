# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings

from .views import *

urlpatterns = [
    url(r'^auto/(?P<field_name>(model|flavor|vendor|brand|series))$', standard_item_auto_complete, name = 'standards-auto-complete'),
    url(r'^category/(?P<parent_id>[0-9]+)$', standard_item_category_auto_complete, name = 'standards-category'),
    url(r'^series$', standard_item_series_auto_complete, name = 'standards-series'),
    url(r'^extract-tags/(?P<store_id>[0-9]+)$', extract_tags, name = 'standards-extract-tags'),
    url(r'^extract-brands/(?P<store_id>[0-9]+)$', extract_brands, name = 'standards-extract-brands'),
    url(r'^add-tag$', add_tag, name = 'standards-add-tag'),
    url(r'^update-item-keywords$', update_item_keywords, name = 'standards-update-item-keywords'),
    url(r'^match-store-items/(?P<store_id>[0-9]+)/(?P<brand_tag_id>[0-9]+)$', match_store_items, name = 'standards-match-store-items'),
    url(r'^tagging/search-items$', search_items, name = 'standards-tagging-search-items'),
    url(r'^map-store-category-to-std-category/(?P<store_category_id>[0-9]+)$', map_store_category_to_standard_category, name = 'standards-map-store-cateogyr-to-standard-category'),
]

