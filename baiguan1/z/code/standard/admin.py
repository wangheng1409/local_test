# -*- coding: utf-8 -*-
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone

from .forms import *
from .models import *

from operator import or_, and_
import preprocessing
import requests
import lxml.html
from lxml import etree

class CategoryAdmin(admin.ModelAdmin):
    form = CategoryForm
    list_display = ('id', 'name', 'parent', 'level', 'created_at')
    list_filter = ('level', )
    search_fields = ('name', )
    raw_id_fields = ('parent', )

    def get_queryset(self, request):
        qs = super(CategoryAdmin, self).get_queryset(request).select_related('parent')
        return qs

def update_standard_name(modeladmin, request, queryset):
    standard_name = request.POST.get('standard_name', '')
    standard_name = standard_name.strip()
    if len(standard_name) > 0:
        queryset.update(standard_name = standard_name, last_updated=timezone.now(), status='human_verified', operator=request.user)
        modeladmin.message_user(request, (u'已更新了 %d 条记录') % (queryset.count(),), messages.SUCCESS)

    else:
        modeladmin.message_user(request, (u'更新失敗. 企业简称不能留空') , messages.ERROR)
update_standard_name.short_description = u'更新企业简称'

def mark_na(modeladmin, request, queryset):
    num = queryset.update(status = 'na', operator=request.user)
    modeladmin.message_user(request, '%s 个商品成功更改状态' % num)
mark_na.short_description = u'批量更改状态为 不处理'

def mark_verified(modeladmin, request, queryset):
    num = queryset.update(status = 'human_verified', operator=request.user)
    modeladmin.message_user(request, '%s 个商品成功更改状态' % num)
mark_verified.short_description = u'批量更改状态为 已通过人工审核'

class StandardCompanyAdmin(admin.ModelAdmin):
    form = StandardCompanyForm
    list_display = ('id', 'name_link', 'num_vendors', 'complete_rate', 'show_num_sku', 'num_pending_items', 'num_verified_items', 'num_new', 'num_na', 'last_updated')
    list_filter = ('last_updated', )
    search_fields = ('name', )
    readonly_fields = ('name', 'num_vendors', 'complete_rate', 'num_sku', 'num_pending_items', 'num_verified_items', 'num_new', 'num_na', 'last_updated')

    def name_link(self, obj):
        return u'<a href="/cma/standard/standarditem/?vendor_short_name_txt=%s" target="_blank">%s</a>' % (obj.name, obj.name)
    name_link.allow_tags = True
    name_link.short_description = u'企业简称'

    def show_num_sku(self, obj):
        return u'<a href="%s?brand=%s" target="_blank">%s</a>' % (reverse('monitor-brand-items'), obj.name, obj.num_sku)
    show_num_sku.allow_tags = True
    show_num_sku.short_description = u'SKU'
    show_num_sku.admin_order_field = 'num_sku'

    def get_queryset(self, request):
        qs = super(StandardCompanyAdmin, self).get_queryset(request)
        return qs.order_by('-num_sku')

class StandardVendorAdmin(admin.ModelAdmin):
    form = StandardVendorForm
    list_display = ('id', 'barcode_link', 'status', 'name', 'standard_name', 'show_sku', 'operator', 'last_updated')
    list_filter = ('status', )
    search_fields = ('barcode', 'name', 'standard_name', 'operator__username')
    readonly_fields = ('read_barcode', 'baidu_result', 'top_20_items')
    action_form = StandardVendorUpdateActionForm
    actions = [update_standard_name, mark_na]

    # def get_action_choices(self, request, default_choices=''):
    #     print default_choices
    #     choices = []
    #     print self.get_actions(request)
    #     # for func, name, description in self.get_actions(request):
    #     #     choice = (name, description % model_format_dict(self.opts))
    #     #     choices.append(choice)
    #     return choices

    # def get_actions(self, request):
    #     actions = super(StandardVendorAdmin, self).get_actions(request)
    #     del actions['delete_selected']
    #     return actions

    def get_search_results(self, request, queryset, search_term):
        out_queryset, use_distinct = super(StandardVendorAdmin, self).get_search_results(request, queryset, search_term)
        search_words = search_term.split(',')
        if len(search_words) > 0:
            for field in self.search_fields:
                q_objects = []
                for word in search_words:
                    q_objects.append(Q(**{field + '__icontains': word.strip()}))
                out_queryset |= queryset.filter(reduce(and_, q_objects))
        return out_queryset, use_distinct

    def barcode_link(self, obj):
        return '<a href="%s/change" target="_blank">%s</a>' % (obj.pk, obj.barcode)
    barcode_link.allow_tags = True
    barcode_link.short_description = u'国际条码'

    def show_sku(self, obj):
        return u'<a href="/cma/standard/standarditem/?q=%s" target="_blank">%s</a>' % (obj.barcode, obj.num_sku)
    show_sku.allow_tags = True
    show_sku.short_description = u'SKU'
    show_sku.admin_order_field = 'num_sku'

    def read_barcode(self, obj):
        return obj.barcode
    read_barcode.short_description = u'条码'

    def baidu_result(self, obj):
        return '<a href="https://www.baidu.com/s?wd=%s" target="_blank">GO</a>' % obj.name
    baidu_result.allow_tags = True
    baidu_result.short_description = u'百度搜'

    def top_20_items(self, obj):
        sis = StandardItem.objects.filter(barcode__startswith=obj.barcode)[:20]
        out = []
        for s in sis:
            out.append('%s\n' % s.name)
        return '<pre style="clear: both;">\n%s</pre>' % ''.join(out)
    top_20_items.allow_tags = True
    top_20_items.short_description = u'商品'

    def get_queryset(self, request):
        qs = super(StandardVendorAdmin, self).get_queryset(request).select_related('operator')
        return qs.order_by('-num_sku')

    def save_model(self, request, obj, form, change):
        instance = form.save(commit=False)
        instance.operator = request.user
        instance.status='human_verified'
        instance.save()
        return instance

def batch_update_category(modeladmin, request, queryset):
    id_raw_list = queryset.values_list('id', flat=True)
    ids = ['id=%s' % k for k in id_raw_list]
    ids = '&'.join(ids)
    return redirect('%s?%s' % (reverse('standards-vendor-series-category-batch-update'), ids))
batch_update_category.short_description = u'批量更新 对应商品分类'

class StandardSeriesAdmin(admin.ModelAdmin):
    form = StandardSeriesForm
    list_display = ('id', 'update', 'vendor_short_name', 'brand', 'series', 'category', 'operator', 'last_updated')
    list_filter = ('status', )
    search_fields = ('vendor_short_name', 'brand', 'series', 'category__name', 'operator__username')
    raw_id_fields = ('category', 'operator')
    actions = [batch_update_category, mark_na, mark_verified]

    def get_queryset(self, request):
        qs = super(StandardSeriesAdmin, self).get_queryset(request).select_related('operator', 'category')
        return qs

    def update(self, obj):
        return '<a href="%s" target="_blank">%s</a>' % ('%s?id=%s' % (reverse('standards-vendor-series-category-batch-update'), obj.pk), obj.get_status_display())
    update.allow_tags = True
    update.short_description = u'状态'

    def save_model(self, request, obj, form, change):
        instance = form.save(commit=False)
        instance.operator = request.user
        instance.save()
        return instance

    def get_search_results(self, request, queryset, search_term):
        out_queryset, use_distinct = super(StandardSeriesAdmin, self).get_search_results(request, queryset, search_term)
        search_words = search_term.split(',')
        if len(search_words) > 0:
            for field in self.search_fields:
                q_objects = []
                for word in search_words:
                    q_objects.append(Q(**{field + '__icontains': word.strip()}))
                out_queryset |= queryset.filter(reduce(and_, q_objects))
        return out_queryset, use_distinct

def update_fields(modeladmin, request, queryset):
    id_raw_list = queryset.values_list('id', flat=True)
    ids = ['id=%s' % k for k in id_raw_list]
    ids = '&'.join(ids)
    return redirect('%s?%s' % (reverse('standards-review-batch-item'), ids))
update_fields.short_description = u'批量更改 系列'

class StandardItemAdmin(admin.ModelAdmin):
    form = StandardItemForm
    list_display = ('id', 'show_barcode', 'get_status', 'show_num_matches', 'name', 'get_tags', 'model', 'flavor', 'vendor_short_name_txt', 'brand_txt', 'series_txt', 'category_txt', 'operator', 'last_updated')
    list_filter = ('status', )
    search_fields = ('barcode', 'name', 'vendor_txt', 'vendor_short_name_txt', 'brand_txt', 'series_txt', 'category_txt', 'keywords', 'operator__username')
    readonly_fields = ('show_barcode', 'get_alias', 'vendor_short_name_txt', 'brand_txt', 'series_txt', 'category_txt', 'get_keywords', )
    raw_id_fields = ('category', 'series')
    actions = [update_fields, mark_na, mark_verified]

    def get_tags(self, obj):
        if obj.keywords:
            return ', '.join(obj.keywords)
        return '-'
    get_tags.allow_tags = True
    get_tags.short_description = u'标签'
    get_tags.admin_order_field = 'keywords'

    def show_num_matches(self, obj):
        return u'<a href="/cma/store/filteredstoreitem/?standard_item_id=%s" target="_blank">%s</a>' % (obj.id, obj.num_matches)
    show_num_matches.allow_tags = True
    show_num_matches.short_description = u'匹配商品数'
    show_num_matches.admin_order_field = 'num_matches'

    def show_barcode(self, obj):
        if obj.barcode:
            return u'<a href="%s" target="_blank">%s</a>' % (reverse('standards-review-ancc-forward', kwargs={'barcode': obj.barcode}), obj.barcode)
        else:
            return u'-'
    show_barcode.allow_tags = True
    show_barcode.short_description = u'条码'
    show_barcode.admin_order_field = 'barcode'

    def get_search_results(self, request, queryset, search_term):
        out_queryset, use_distinct = super(StandardItemAdmin, self).get_search_results(request, queryset, search_term)
        # print queryset.count()
        # print out_queryset.count()
        # print '....'
        search_words = search_term.split(u',')
        if len(search_words) > 0:
            for field in self.search_fields:
                q_objects = []
                for word in search_words:
                    print type(word)
                    keyword = word.strip()
                    # print '%s__icontains="%s"' % (field, keyword)
                    q_objects.append(Q(**{field + '__icontains': keyword}))
                sub_queryset = queryset.filter(reduce(and_, q_objects))
                # print sub_queryset.count()
                out_queryset |= sub_queryset
        # print out_queryset.count()
        return out_queryset, use_distinct

    def get_status(self, obj):
        return u'<a href="%s" target="_blank">%s</a>' % (reverse('standards-review-item', kwargs={'pk': obj.pk}), obj.get_status_display())
    get_status.allow_tags = True
    get_status.short_description = u'状态'

    def get_keywords(self, obj):
        if obj.keywords:
            return u'%s' % ', '.join(obj.keywords)
        return u'保存后自动生成'
    get_keywords.allow_tags = True
    get_keywords.short_description = u'关键词'

    def get_alias(self, obj):
        if obj.alias:
            return u"""
            <div style="width:400px; height:200px; overflow-y:scroll">%s</div>
            <style>.submit-row {
                position: fixed;
                bottom: 10px;
                right: 50px;
            }</style>""" % '<br>'.join(obj.alias)
        # return u'从国条小店采集回来'
        return u'-'
    get_alias.allow_tags = True
    get_alias.short_description = u'別名'

    def get_queryset(self, request):
        qs = super(StandardItemAdmin, self).get_queryset(request).select_related('operator')
        return qs.order_by('-num_matches')

    def save_model(self, request, obj, form, change):
        instance = form.save(commit=False)
        p_item = preprocessing.models.Item(instance.name)
        instance.keywords = p_item.keywords
        instance.operator = request.user
        instance.save()
        return instance

### http://stackoverflow.com/questions/2223375/multiple-modeladmins-views-for-same-model-in-django-admin
# class VerifiedStandardItemAdmin(PendingReviewStandardItemAdmin):
#     def get_queryset(self, request):
#         return self.model.objects.filter(status = 'verified')

class StandardTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'type', 'pinyin')
    search_fields = ('tag', 'pinyin', 'alias')
    list_filter = ('type', )
    readonly_fields = ('pinyin', 'alias')

admin.site.register(Category, CategoryAdmin)
admin.site.register(StandardSeries, StandardSeriesAdmin)
admin.site.register(StandardVendor, StandardVendorAdmin)
admin.site.register(StandardItem, StandardItemAdmin)
admin.site.register(StandardCompany, StandardCompanyAdmin)
admin.site.register(StandardTag, StandardTagAdmin)



