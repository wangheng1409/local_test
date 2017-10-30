# -*- coding: utf-8 -*-
from django.contrib import admin

from .forms import *
from .models import *

# class DailyStoreItemSummaryAdmin(admin.ModelAdmin):
#     form = DailyStoreItemSummaryForm
#     list_display = ('date', 'item', 'sales', 'num', 'barcode', 'model', 'flavor', 'category', 'last_updated')
#     search_fields = ('item__name', )
#     raw_id_fields = ('item', )

# class DailyStoreSummaryAdmin(admin.ModelAdmin):
#     form = DailyStoreSummaryForm
#     list_display = ('date', 'store', 'sales', 'num', 'num_sku', 'last_updated')
#     search_fields = ('store__name', )
#     raw_id_fields = ('store', )

class MonthlyStoreItemPatternAdmin(admin.ModelAdmin):
    list_display = ('date', 'store', 'show_patterns', 'frequency', 'last_updated')
    search_fields = ('store__name', )
    raw_id_fields = ('store', )
    readonly_fields = ('date', 'store', 'patterns', 'frequency')

    def show_patterns(self, obj):
        if obj.patterns:
            return ', '.join(obj.patterns)
        return u'-'
    show_patterns.short_description = u'同时购买商品'
    show_patterns.admin_order_field = 'patterns'

    def get_queryset(self, request):
        qs = super(MonthlyStoreItemPatternAdmin, self).get_queryset(request).select_related('store')
        return qs.order_by('-frequency')


# admin.site.register(DailyStoreItemSummary, DailyStoreItemSummaryAdmin)
# admin.site.register(DailyStoreSummary, DailyStoreSummaryAdmin)
admin.site.register(MonthlyStoreItemPattern, MonthlyStoreItemPatternAdmin)
