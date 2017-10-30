# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from summary.views import *
from standard.views import *
from store.views import *
from monitor.views import *
from advertisement.views import *
from discovery.views import *

admin.autodiscover()
admin.site.site_header = u'超盟'
admin.site.site_title = u'超盟'
admin.site.index_title = u'超盟'



urlpatterns = [
    url(r'^cma/', include(admin.site.urls)),
    url(r'^login/$', auth_views.login, {'template_name': 'user/login.html'}, name='login'),

    url(r'^extract_test$', extract_item_meta, name = 'standard-extract-item-meta'),
    url(r'^daily/(?P<date>[0-9]{4}\-[0-9]{2}\-[0-9]{2})/store/(?P<store_pk>[0-9]+)$', daily_store_category_sales, name = 'summary-daily-store-category-sales'),
    url(r'^daily/(?P<date>[0-9]{4}\-[0-9]{2}\-[0-9]{2})/store/(?P<store_pk>[0-9]+)/detail$', daily_store_category_sales_detail, name = 'summary-daily-store-category-sales-detail'),

    url(r'^monthly/(?P<date>[0-9]{4}[0-9]{2})/store/(?P<store_pk>[0-9]+)$', monthly_store_category_sales, name = 'summary-monthly-store-category-sales'),
    url(r'^monthly/(?P<date>[0-9]{4}\-[0-9]{2})/store/(?P<store_pk>[0-9]+)/combine$', monthly_store_category_sales_combine, name = 'summary-monthly-store-category-sales-combine'),
    url(r'^monthly/(?P<date>[0-9]{4}\-[0-9]{2})/store/(?P<store_pk>[0-9]+)/vendor-rank$', monthly_store_category_sales_vendor_rank, name = 'summary-monthly-store-category-sales-vendor-rank'),
    url(r'^monthly/(?P<date>[0-9]{4}\-[0-9]{2})/store/(?P<store_pk>[0-9]+)/vendor-model$', monthly_store_category_sales_vendor_model, name = 'summary-monthly-store-category-sales-vendor-model'),
    url(r'^monthly/(?P<date>[0-9]{4}\-[0-9]{2})/store/(?P<store_pk>[0-9]+)/model-brand$', monthly_store_category_sales_model_brand, name = 'summary-monthly-store-category-sales-model-brand'),
    url(r'^monthly/(?P<date>[0-9]{4}\-[0-9]{2})/store/(?P<store_pk>[0-9]+)/vendor-flavor$', monthly_store_sales_vendor_model_flavor, name = 'summary-monthly-store-sales-vendor-model-flavor'),

    url(r'^$', empty_home, name = 'empty-home'),
    url(r'^summary/(?P<date>[0-9]{4}\-[0-9]{2})$', by_month_summary, name = 'summary-by-month-summary'),
    url(r'^monthly/(?P<date>[0-9]{4}\-[0-9]{2})/stores$', monthly_store_list, name = 'monthly-store-list'),
    url(r'^monthly/(?P<date>[0-9]{4}\-[0-9]{2})/combine$', monthly_category_sales_combine, name = 'summary-monthly-category-sales-combine'),
    url(r'^monthly/(?P<date>[0-9]{4}\-[0-9]{2})/vendor-rank$', monthly_category_sales_vendor_rank, name = 'summary-monthly-category-sales-vendor-rank'),
    url(r'^monthly/(?P<date>[0-9]{4}\-[0-9]{2})/vendor-model$', monthly_category_sales_vendor_model, name = 'summary-monthly-category-sales-vendor-model'),
    url(r'^monthly/(?P<date>[0-9]{4}\-[0-9]{2})/model-brand$', monthly_category_sales_model_brand, name = 'summary-monthly-category-sales-model-brand'),
    url(r'^monthly/(?P<date>[0-9]{4}\-[0-9]{2})/vendor-flavor$', monthly_sales_vendor_model_flavor, name = 'summary-monthly-sales-vendor-model-flavor'),
    # url(r'^new-products$', new_products, name = 'new-products-home'),
    url(r'^new-products/(?P<date>[0-9]{4}\-[0-9]{2})$', new_products_v2, name = 'new-products-monitoring'),
    url(r'^new-products/$', new_products_home, name = 'new-products'),

    ####
    url(r'^summary/(?P<date>[0-9]{4}\-[0-9]{2})/detail$', summary_detail, name = 'summary-detail'),
    url(r'^summary/(?P<date>[0-9]{4}\-[0-9]{2})/vendor-rank$', summary_vendor_rank, name = 'summary-vendor-rank'),


    ### store_items -> standard_items
    url(r'^matches/(?P<item_pk>[0-9]+)$', matches, name = 'item-matches'),
    url(r'^matches/mark-status/(?P<item_pk>[0-9]+)/(?P<status>(na|new))$', mark_status, name = 'item-matches-mark-status'),
    url(r'^si-searches$', search_standard_items, name = 'standard-items-searchs'),

    ### review pending standard_items
    url(r'^standards/items/(?P<pk>[0-9]+)$', review_standard_item, name = 'standards-review-item'),
    url(r'^standards/items/batch-update$', batch_review_standard_item, name = 'standards-review-batch-item'),
    url(r'^standards/vendor-series-category/batch-update$', batch_review_standard_vendor_series_category, name = 'standards-vendor-series-category-batch-update'),
    url(r'^ancc-forward/(?P<barcode>[0-9]+)$', ancc_forward, name = 'standards-review-ancc-forward'),
    url(r'^ancc-vendor-forward/(?P<barcode>[0-9]+)$', ancc_vendor_forward, name = 'standards-review-ancc-vendor-forward'),

    url(r'^monitor/brand-items$', monitor_brand_items, name = 'monitor-brand-items'),

    url(r'^sku$', store_sku_comparison, name = 'store-sku-comparison'),

    ## DO NOT REMOVE.
    url(r'^ads$', ads, name='ads-sample'),
    url(r'^cma/store/store-topitem$', store_top_item_view, name='store_top_item_view'),
    url(r'^cma/store/store-topitemdetail$', store_top_item_detail_view, name='store_top_item_detail_view'),
    url(r'^cma/store/store-categorynearbyview$', store_category_nearby_view, name='store_category_nearby_view'),
    url(r'^cma/store/store-pricesview$', store_prices_view, name='store_prices_view'),
    url(r'^cma/store/store-analysisview$', store_analysis_view, name='store_analysis_view'),
    url(r'^cma/store/store-basketquadrantview$', store_basket_quadrant_view, name='store_basket_quadrant_view'),
    url(r'^cma/store/store-basketcategoryview$', store_basket_category_view, name='store_basket_category_view'),
    url(r'^cma/store/store-basketweekview$', store_basket_week_view, name='store_basket_week_view'),
    url(r'^cma/store/store-basketsalesview$', store_basket_sales_view, name='store_basket_sales_view'),

    url(r'^advertisement$', print_demo_receipts, name='advertisement'),
    url(r'^search_districts/(?P<query>\w*)$', search_districts, name='search_districts'),
    url(r'^add_advertisement$', add_advertisement, name='add_advertisement'),
    url(r'^show_receipt_template$', show_receipt_template, name='show_receipt_template'),
    url(r'^template_image/(?P<filename>tmp/\w*.\w*)$', template_image, name='template_image'),
    url(r'^advertising_detail$', advertising_detail, name='advertising_detail'),
    url(r'^approve_ad$', approve_advertisement, name='approve_advertisement'),

    url(r'^store/(?P<store_id>[0-9]+)/update-shelf$', store_update_shelf, name='store-update-shelf'),
    url(r'^store/(?P<store_id>[0-9]+)/items-searches$', store_item_search, name = 'store-item-search'),

    url(r'^discovery$', find_new_good, name = 'find-new-good'),
    url(r'^collect$', collect_commodity, name = 'collect-commodity'),
    url(r'^product-info$', product_info, name = 'product-info'),

    url(r'^api/v1/products-category$', products_category, name = 'products-category'),
    url(r'^product-collect$', product_collect, name = 'product-collect'),
    url(r'^collected-product$', collected_product, name = 'collected-product'),
    url(r'^api/v1/products-list-collected$', product_list_collected, name = 'product-list-collected'),

    url(r'^api/v1/online-item',
        login_required(OnlineItem.as_view()),
        name='v1-api-online-item'),

    url(r'^operational_analysis/(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})$', operational_analysis,name='operational_analysis'),
    url(r'^store/store-comparison/(?P<stores>([0-9]+)-([0-9]+)(-[0-9]+)*)$', store_comparison, name='store-comparison'),
    url(r'^integration/add-transaction-accounts$', add_transaction_accounts, name='add_transaction_accounts'),
    url(r'^integration/navigation$', navigation, name='navigation'),

    url(r'^api/v1/online-item', login_required(OnlineItem.as_view()), name='v1-api-online-item'),
    url(r'^analytics/', include('analytics.urls')),
    url(r'^standards/', include('standard.urls')),
    url(r'^integration/add-db', third_party_db_info_page,
        name='add-third-party-data-source-db-info'),
    url(r'^api/v1/thirdpartydb',
        login_required(ThirdPartyDBAPI.as_view()),
        name='v1-api-thirdparyt-db'),
    
    url(r'^monitor/monitor-spider$', monitor_spider, name = 'monitor-spider'),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    ]

