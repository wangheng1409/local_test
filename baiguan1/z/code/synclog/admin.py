# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *

class StoreItemSyncLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_id', 'count', 'created_at')
    search_fields = ('last_id', )

class BarcodeStoreItemSyncLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_id', 'count', 'created_at')
    search_fields = ('last_id', )

class WebFoodSafetyBarcodeSyncLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_date', 'count', 'created_at')
    search_fields = ('last_date', )

class SpiderSyncLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'source', 'area', 'crawl_date', 'tag', 'count')
    search_fields = ('source', 'area', 'crawl_date', 'tag')

admin.site.register(StoreItemSyncLog, StoreItemSyncLogAdmin)
admin.site.register(BarcodeStoreItemSyncLog, BarcodeStoreItemSyncLogAdmin)
admin.site.register(WebFoodSafetyBarcodeSyncLog, WebFoodSafetyBarcodeSyncLogAdmin)
admin.site.register(SpiderSyncLog, SpiderSyncLogAdmin)
