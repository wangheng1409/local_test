# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.utils.html import format_html

from .forms import *
from .models import *
from standard.models import StandardItem
from core.export import export_queryset_as_csv
from advertisement.models import Printer


class CityAdmin(admin.ModelAdmin):
    form = CityForm
    list_display = ('id', 'name', 'parent_id', 'level')
    search_fields = ('name',)


class TradingAreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'city', 'name')
    search_fields = ('city__name', 'name')


class StoreTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


class CustomerTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

class PrinterInline(admin.TabularInline):
    model = Printer
    extra = 0

class StoreAdmin(admin.ModelAdmin):
    # change_form_template = 'admin/store_change_form.html'
    inlines = [PrinterInline, ]
    form = StoreForm
    list_display = (
        'store_id', 'store_name', 'trading_area', 'show_tags', 'show_customer_types', 'complete_rate',
        'num_pending_items',
        'num_sku', 'num_verified_items', 'num_new_items', 'num_na', 'last_updated')
    list_filter = ('store_scale', 'receipt_printing_freq', 'bussiness_hours')
    search_fields = ('name', 'address', 'city_path')
    raw_id_fields = ('trading_area',)
    readonly_fields = ('name', 'address', 'location', 'contact_name', 'contact_phone', 'bussiness_hours', 'store_scale',
                       'receipt_printing_freq')

    fieldsets = (
        (u'标签', {
            'fields': ('tags', 'customer_types', 'trading_area'),
            # 'description': desc
        }),
        (u'商店明細', {
            'fields': ('name', 'address', 'location', 'contact_name', 'contact_phone', 'bussiness_hours', 'store_scale',
                       'receipt_printing_freq',),
            # 'description': desc
        }),
    )

    def show_tags(self, obj):
        if obj.tags:
            return ', '.join([self.tags_map[v] for v in obj.tags])
        return u'-'

    show_tags.short_description = u'标签'
    show_tags.admin_order_field = 'tags'

    def show_customer_types(self, obj):
        if obj.customer_types:
            return ', '.join([self.customers_map[v] for v in obj.customer_types])
        return u'-'

    show_customer_types.short_description = u'覆盖人群'
    show_customer_types.admin_order_field = 'customer_types'

    def location(self, obj):
        if obj.lat and obj.lng:
            return u'<a href="http://map.baidu.com/?latlng=%f,%f&title=%s&content=%s&autoOpen=true&l" target="_blank">地理位置</a>' % (
                obj.lat, obj.lng, obj.name, obj.address)
        return u'-'

    location.allow_tags = True
    location.short_description = u'商店'

    def store_name(self, obj):
        return u'<a href="/cma/store/storecompanystats/?store_id=%s" target="_blank">%s</a> | <a href="/cma/store/filteredstoreitem/?store_id=%s" target="_blank">ALL<a/> |<a href="%s?store_id=%s" target="_blank">单店分析</a>' % (obj.store_id, obj.name, obj.store_id, reverse('store_analysis_view'),obj.store_id)
    store_name.allow_tags = True
    store_name.short_description = u'商店'
    store_name.admin_order_field = 'name'

    def get_queryset(self, request):
        qs = super(StoreAdmin, self).get_queryset(request).select_related('trading_area', 'trading_area__city')
        self.tags_map = dict(list(StoreTag.objects.values_list('id', 'name')))
        self.customers_map = dict(list(CustomerType.objects.values_list('id', 'name')))
        return qs.order_by('-num_new_items')


class StoreCompanyStatsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'show_company_items', 'complete_rate', 'num_sku', 'num_pending_items', 'num_verified_items', 'num_new',
        'num_na', 'show_store_name', 'last_updated')
    list_filter = ('last_updated',)
    search_fields = ('company__name', 'company__id', 'store__id', 'store__name')
    readonly_fields = (
        'store', 'company', 'complete_rate', 'num_sku', 'num_pending_items', 'num_verified_items', 'num_new', 'num_na')

    def get_queryset(self, request):
        qs = super(StoreCompanyStatsAdmin, self).get_queryset(request).select_related('store', 'company')
        return qs.order_by('-complete_rate')

    def show_store_name(self, obj):
        return obj.store.name

    show_store_name.allow_tags = True
    show_store_name.short_description = u'商店'

    def show_company_items(self, obj):
        return u'<a href="/cma/store/filteredstoreitem/?store_id=%s&company_id=%s" target="_blank"<>%s</a>' % (
            obj.store.store_id, obj.company.id, obj.company.name)

    show_company_items.allow_tags = True
    show_company_items.short_description = u'品牌'
    show_company_items.admin_order_field = 'company'


class StoreItemAdmin(admin.ModelAdmin):
    form = StoreItemForm
    list_display = ('name', 'receipt_item_id', 'price', 'status', 'store_name', 'trade_at', 'last_updated')
    list_filter = ('status', 'trade_at')
    raw_id_fields = ('store', 'standard_item')
    search_fields = ('name', 'store__id', 'store__name')
    readonly_fields = ('name', 'price', 'store', 'trade_at', 'last_updated')

    def name(self, obj):
        return u'%s' % obj.name

    name.allow_tags = True

    def price(self, obj):
        return u'%s' % obj.price

    price.allow_tags = True

    def store(self, obj):
        if obj.store:
            return u'%s' % obj.store.name
        return u'-'

    store.allow_tags = True

    def store_name(self, obj):
        if obj.store:
            if len(obj.store.name) > 10:
                return u'<span title="%s">%s...</span>' % (obj.store.name, obj.store.name[:10])
            else:
                return u'%s' % obj.store.name[:10]

        return u'-'

    store_name.allow_tags = True

    def trade_at(self, obj):
        if obj.trade_at:
            return u'%s' % obj.trade_at
        return u'-'

    trade_at.allow_tags = True

    def last_updated(self, obj):
        if obj.last_updated:
            return u'%s' % obj.last_updated
        return u'-'

    last_updated.allow_tags = True

    def get_queryset(self, request):
        return self.model.objects.filter(Q(status='pending_review') | Q(status='human_verified'))


class FilteredStoreItem(StoreItem):
    class Meta:
        proxy = True
        verbose_name = u'所有商品'
        verbose_name_plural = u'所有商品'


def mark_pending(self, request, queryset):
    num = queryset.update(status='pending_review', operator=request.user)
    self.message_user(request, '%s 个商品成功更改状态' % num)


mark_pending.short_description = u'更改状态为 待审核'


def mark_human_verified(self, request, queryset):
    num = queryset.update(status='human_verified', operator=request.user)
    self.message_user(request, '%s 个商品成功更改状态' % num)


mark_human_verified.short_description = u'更改状态为 已通过人工审核'


def mark_na(self, request, queryset):
    num = queryset.update(status='na', operator=request.user)
    self.message_user(request, '%s 个商品成功更改状态' % num)


mark_na.short_description = u'更改状态为 不处理'


def mark_new(self, request, queryset):
    num = queryset.update(status='new', operator=request.user)
    self.message_user(request, '%s 个商品成功更改状态' % num)


mark_new.short_description = u'更改状态为 新增商品'


class FilteredStoreItemAdmin(admin.ModelAdmin):
    form = StoreItemForm
    list_display = (
        'id', 'status', 'item_name', 'price', 'matched_item_name', 'company', 'receipt_item_id', 'store_name',
        'operator',
        'trade_at')
    list_filter = ('status',)
    raw_id_fields = ('store', 'standard_item')
    search_fields = ('name', 'operator__username', 'receipt_item_id')
    actions = [export_queryset_as_csv, mark_human_verified, mark_pending, mark_na, mark_new]
    export_fields = ('name', 'price', 'store_name')

    def get_queryset(self, request):
        store_id = request.GET.get('store_id')
        if store_id:
            return self.model.objects.filter(store__id=request.GET.get('store_id')).select_related('standard_item',
                                                                                                   'store', 'company')
        return self.model.objects.all().select_related('standard_item', 'store')

    def item_name(self, obj):
        return '<a href="%s" target="_blank">%s</a>' % (reverse('item-matches', kwargs={'item_pk': obj.id}), obj.name)

    item_name.allow_tags = True
    item_name.short_description = u'审核'
    item_name.admin_order_field = 'name'

    def matched_item_name(self, obj):
        if obj.standard_item:
            return obj.standard_item.name
        return '-'

    matched_item_name.allow_tags = True
    matched_item_name.short_description = u'匹配到'

    def store_name(self, obj):
        if obj.store:
            if len(obj.store.name) > 10:
                return u'<span title="%s">%s...</span>' % (obj.store.name, obj.store.name[:10])
            else:
                return u'%s' % obj.store.name[:10]
        return u'-'

    store_name.allow_tags = True
    store_name.short_description = u'商店名'
    store_name.admin_order_field = 'store__name'

class StoreShelfAdmin(admin.ModelAdmin):
    list_display = ('store', 'shelf_id', 'created_at')
    list_filter = ('created_at', )
    raw_id_fields = ('store', )
    search_fields = ('shelf_id', 'store__id', 'store__name')

class EntityAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'type', 'entity_districts', 'location', 'address', 'telephone', 'has_added_to_contact_list',
        'add_to_compare_list')
    list_display_links = ()
    list_filter = ('type',)
    search_fields = ('name', 'address')
    readonly_fields = (
        'name', 'type', 'address', 'city_path', 'lat', 'lng', 'address', 'telephone', 'amap_id', 'baidu_map_id')

    def add_to_contact_list(self, request, queryset):
        result = []
        for item in queryset:
            CooperativeEntity.objects.get_or_create(entity=item)
            result.append(item.name)
        self.message_user(request, u'%s 个商家已经成功加入待联系列表' % queryset.count())

    add_to_contact_list.short_description = u'添加至联系列表'

    def similarity_compare(self, request, queryset):
        ids = [item.id for item in queryset]

    similarity_compare.short_description = u'商店比较'

    actions = [add_to_contact_list, similarity_compare]

    def has_add_permission(self, request):
        return False

    def entity_districts(self, obj):
        city_path = obj.city_path
        if city_path:
            result = ''
            city_path = city_path.split('>')
            for city_id in city_path:
                city = City.objects.filter(id=int(city_id))[0].name
                result += city
            return result

    entity_districts.short_description = u'所在区域'
    entity_districts.admin_order_field = 'city_path'

    def has_added_to_contact_list(self, obj):
        if CooperativeEntity.objects.filter(entity_id=obj.id).count() > 0:
            return True
        return False

    has_added_to_contact_list.allow_tags = True
    has_added_to_contact_list.short_description = u'添加至联系列表'

    def add_to_compare_list(self, obj):
        if obj.type.startswith('06'):
            return format_html(u'<input type="button" id="{}" value="{}"/>', obj.id, u'单店数据分析')

    add_to_compare_list.short_description = u'操作'

    def location(self, obj):
        lng = obj.lng
        lat = obj.lat
        name = obj.name
        amap_url = 'http://m.amap.com/navi/?dest=%s,%s&destName=%s&key=9d5f7733617e3fd450af5aa48a881810' % (
            lng, lat, name)

        return u'<a href="%s">高德地图</a> | <a href="">百度地图</a>' % amap_url

    location.allow_tags = True
    location.short_description = u'查看地图'

    class Media:
        js = (
            'lib/jquery-3.0.0.min.js',
            'lib/layer/layer.js',
            'js/store/add_to_compare_list.js'
        )


class CooperativeEntityAdmin(admin.ModelAdmin):
    list_display = ['entity', 'dialed', 'has_pos', 'all_print', 'printer_installed', 'postscript']

    def has_add_permission(self, request):
        return False

class ChainStoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'show_category', 'owner')

    def show_category(self, obj):
        return u'<a href="/cma/store/storecategory/?store_id=%s">查看分類</a>' % obj.id
    show_category.allow_tags = True
    show_category.short_description = u'查看分類'



class StoreCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'match', 'parent', 'level', 'store', 'operator', 'last_updated')
    list_filter = ('level',)
    raw_id_fields = ('store', 'std_category')

    def match(self, obj):
        if obj.std_category:
            val = u'<span style="color:#21ba45">%s' % obj.std_category
        else:
            val = u'<span style="color:#db2828">配匹</span>'
        return u'<a href="%s" target="_blank">%s</a>' % (reverse('standards-map-store-cateogyr-to-standard-category', kwargs={'store_category_id': obj.id}), val)
    match.allow_tags = True
    match.short_description = u'标準分類'
    match.admin_order_field = 'std_category'


admin.site.register(City, CityAdmin)
admin.site.register(TradingArea, TradingAreaAdmin)
admin.site.register(CustomerType, CustomerTypeAdmin)
admin.site.register(StoreTag, StoreTagAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(StoreCompanyStats, StoreCompanyStatsAdmin)
admin.site.register(FilteredStoreItem, FilteredStoreItemAdmin)
admin.site.register(Entity, EntityAdmin)
admin.site.register(CooperativeEntity, CooperativeEntityAdmin)
admin.site.register(StoreShelf, StoreShelfAdmin)
admin.site.register(ChainStore, ChainStoreAdmin)
admin.site.register(StoreCategory, StoreCategoryAdmin)

