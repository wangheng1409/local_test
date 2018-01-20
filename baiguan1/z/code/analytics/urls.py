# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings

from .views import *

urlpatterns = [
    url(r'^stores/(?P<store_id>[0-9]+)$', store_items_analytics, name = 'analytics-stores-items'),
    url(r'^stores/(?P<store_id>[0-9]+)/(?P<brand_tag_id>[0-9]+)$', store_brands_analytics, name = 'analytics-stores-brands'),
    url(r'^stores-stores$', stores_stores_compare, name = 'analytics-stores-stores-compare'),
    url(r'^api-stores/(?P<brand_tag_id>[0-9]+)$', web_store_brands_analytics, name = 'analytics-api-stores-brands'),
    url(r'^chain-stores/stores/get-store-list$',stores_list,name="analytics-get-store-list"),
    url(r'^chain-stores/stores/store-detailed-info/special-items/(?P<store_id>\d+)$',store_items,name="analytics-special-commodity"),
    url(r'^chain-stores/store-overview/overall$',overall_data),
    url(r'^chain-stores/store-overview$', store_overview, name = 'analytics-store-overview'),
    url(r'^chain-stores/stores/store-analysis$', store_analysis, name = 'analytics-store-analysis'),
    url(r'^chain-stores/stores/store-detailed-info$', store_detailed_info, name = 'analytics-store-detailed-info'),
    url(r'^chain-stores/stores/(?P<store_id>\d+)/overall$', store_overall_data, name = 'analytics-get-store-overall-data'),
    url(r'^chain-stores/top-items/(?P<store_id>\d+)$', get_store_hot_item, name = 'analytics-get-store-hot-item'),
    url(r'^test$',overall_data)


]