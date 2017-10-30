# -*- coding: utf-8 -*-

from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from django.db import connection

from .forms import *
from .models import *
from store.models import StoreItem, StoreCategory
from preprocessing.utils import rank_standard_items, find_ranking_candidates

import collections
import preprocessing
import json
import requests
import lxml.html
from lxml import etree
import time

from core import sql_utils
import algorithms
import jieba
import pandas

@staff_member_required
def standard_item_category_auto_complete(request, parent_id):
    cursor = connection.cursor()
    sql = """
        select id as value, name from standard_category where parent_id=%s order by parent_id
        """ % parent_id
    cursor.execute(sql)
    out = {'success': True, 'results': sql_utils.dictfetchall(cursor)}

    return HttpResponse(json.dumps(out), content_type="application/json")

@staff_member_required
def standard_item_series_auto_complete(request):
    t1 = request.POST.get('t1', '').strip()
    t2 = request.POST.get('t2', '').strip()

    if len(t1) > 0:
        if len(t2) > 0:
            sql = "SELECT id as value, series as name from standard_standardseries where status='human_verified' and vendor_short_name='%s' and brand='%s';" % (t1, t2)
        else:
            sql = "SELECT distinct brand as value, brand as name from standard_standardseries where status='human_verified' and vendor_short_name='%s'" % t1
    else:
        sql = "SELECT distinct vendor_short_name as value, vendor_short_name as name from standard_standardseries where status='human_verified';"

    cursor = connection.cursor()
    cursor.execute(sql)
    out = {'success': True, 'results': sql_utils.dictfetchall(cursor)}

    return HttpResponse(json.dumps(out), content_type="application/json")


def standard_item_auto_complete(request, field_name):
    form = SearchForm(request.GET or None)
    out = {'results': []}
    if form.is_valid():
        q = form.cleaned_data['q']
        cursor = connection.cursor()
        sql = """
            select distinct %s as name from standard_standarditem where status='human_verified' and %s like '%%%s%%'
            """ % (field_name, field_name, q)
        cursor.execute(sql)
        for raw_row in cursor.fetchall()[:10]:
            out['results'].append({'name': raw_row[0]})

    return HttpResponse(json.dumps(out), content_type="application/json")

@staff_member_required
def review_standard_item(request, pk, template='standard/review.html'):
    instance = StandardItem.objects.get(pk=pk)
    vendor = None
    brand = None
    series = None
    form = ReviewStandardItemForm(request.POST or None, instance = instance)
    msg = None
    if form.is_valid():
        instance = form.save()
        instance.operator = request.user
        instance.save()
        msg = u'更新成功'
    else:
        print form.errors

    if instance.series:
        vendor = instance.series.vendor_short_name
        brand = instance.series.brand
        series = instance.series.id

    return render(request, template, {'form': form, 'instance': instance, 'vendor': vendor, 'brand': brand, 'series': series, 'msg': msg})

@staff_member_required
def batch_review_standard_item(request, template='standard/batch_review.html'):
    ids = request.GET.getlist('id')
    if len(ids) < 0:
        return HttpResponse(u'请选上标品')
    sis = StandardItem.objects.filter(id__in = ids)
    form = StandardItemBatchUpdateForm(request.POST or None)
    msg = None
    if form.is_valid():
        brand = form.cleaned_data['brand']
        series = form.cleaned_data['series']
        update_dict = {}
        if len(brand) > 0:
            update_dict['brand'] = brand
        if len(series) > 0:
            update_dict['series'] = series
            series_obj = StandardSeries.objects.get(pk=series)
            update_dict['series_txt'] = series_obj.series
            update_dict['vendor_short_name_txt'] = series_obj.vendor_short_name
            update_dict['brand_txt'] = series_obj.brand
            update_dict['category_txt'] = series_obj.category.name

        # print update_dict
        if update_dict:
            # update_dict['status'] = 'half_verified'
            sis.update(**update_dict)
        msg = u'更新成功'
    else:
        print form.errors

    return render(request, template, {'sis': sis, 'form': form, 'msg': msg})

@staff_member_required
def ancc_forward(request, barcode):
    r = requests.get('http://101.200.218.39:1111/ancc/%s' % barcode)
    print 'waiting for response...'
    return HttpResponse(r.text)

@staff_member_required
def ancc_vendor_forward(request, barcode):
    url = 'http://search.anccnet.com/searchResult2.aspx'
    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'


    cookies = {
        'ASP.NET_SessionId': 'gr0er545is1f3f5514ytpt55',
        'ASP.NET_SessionId_NS_Sig': 'oenCV6mdznwg-VC_',
    }

    headers = {
        'Origin': 'http://www.ancc.org.cn',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Cache-Control': 'max-age=0',
        'Referer': 'http://www.ancc.org.cn/Service/queryTools/internal.aspx',
        'Connection': 'keep-alive',
    }

    data = '__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=%2FwEPDwULLTE5NTYxNDQyMTkPZBYCAgEPZBYCAhMPFgIeB1Zpc2libGVnFgYCAQ8PFgIeBFRleHQFCDY5MDMxNDgxZGQCAw8PFgIfAGhkZAIFD2QWAgIDDw8WAh4LUmVjb3JkY291bnQCAWRkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYFBRJSYWRpb0l0ZW1Pd25lcnNoaXAFDVJhZGlvSXRlbUluZm8FBlJhZGlvMQUGUmFkaW8yBQZSYWRpbzOGBSruQoGLASsEf3dNgHe7Lv4yKw%3D%3D&__EVENTVALIDATION=%2FwEWCgLDl%2FrsBALLnru%2FBwKB7J3yDAKbg6TuCQLj%2BszOBgLC79P5DgLC78f5DgLC78v5DgLChPy%2BDQLjwOP9CPxkjrTyxPitXCxg%2BTYMC27IPRoN&Top%24h_keyword=&query-condition=RadioItemOwnership&query-supplier-condition=Radio1&txtcode={0}&btn_query=%E6%9F%A5%E8%AF%A2+'.format(barcode)

    r = requests.post('http://www.ancc.org.cn/Service/queryTools/internal.aspx', headers=headers, cookies=cookies, data=data)

    tree = lxml.html.fromstring(r.text)
    out = tree.xpath('//*[@id="searchResult"]')
    return HttpResponse(etree.tostring(out[0]))



@staff_member_required
def extract_item_meta(request, template='standard/extract.html'):
    form = ExtractItemMetaForm(request.POST or None)

    if form.is_valid():
        review_item_name = form.cleaned_data['item_name']

        process_item = preprocessing.models.Item(review_item_name)
        cur = time.time()
        candidates = find_ranking_candidates(review_item_name)
        print 'find candidates: %f' % (time.time() - cur, )

        cur = time.time()
        ranked_candidates_ids, scores = rank_standard_items(candidates, {'name': review_item_name, 'price': 1.0})
        print 'rank candidats: %f' % (time.time() - cur, )

        sis = StandardItem.objects.filter(id__in = ranked_candidates_ids).values('id', 'name', 'num_matches', 'keywords')

        result = collections.OrderedDict()
        for i in range(len(ranked_candidates_ids)):
            result[ranked_candidates_ids[i]] = {'score': round(scores[i] * 100.0, 2)}

        for s in sis:
            result[s['id']]['name'] = s['name']
            result[s['id']]['num_matches'] = s['num_matches']
            result[s['id']]['keywords'] = s['keywords']

        return render(request, template, {'form': form, 'result': result, 'process_item': process_item, 'review_item_name': '', 'candidates_size': len(candidates)})

    return render(request, template, {'form': form})

@staff_member_required
def batch_review_standard_vendor_series_category(request, template='standard/batch_review_standard_series_category.html'):
    ids = request.GET.getlist('id')
    if len(ids) < 0:
        return HttpResponse(u'请选上要更的改系列')
    objects = StandardSeries.objects.filter(id__in = ids)
    form = StandardSeriesBatchUpdateForm(request.POST or None)
    msg = None
    if form.is_valid():
        category_id = form.cleaned_data['category_id']
        update_dict = {}
        if len(category_id) > 0:
            update_dict['category'] = Category.objects.get(pk=category_id)

        if update_dict:
            update_dict['status'] = 'human_verified'
            update_dict['operator'] = request.user
            objects.update('', **update_dict)
        msg = u'更新成功'
    else:
        print form.errors

    return render(request, template, {'objects': objects, 'form': form, 'msg': msg})

@staff_member_required
def extract_tags(request, store_id, template='standard/extract_tags.html'):
    tags = algorithms.extract_tags(store_id)
    return render(request, template, {'tags': tags})

@staff_member_required
def extract_brands(request, store_id, template='standard/extract_brands.html'):
    branded_items, unbranded_items = algorithms.extract_brands(store_id)
    return render(request, template, {'branded_items': branded_items, 'unbranded_items': unbranded_items})

@staff_member_required
@csrf_exempt
def add_tag(request):
    form = StandardTagForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        return HttpResponse('created: %d' % instance.id)

    return HttpResponse(json.dumps([(k, v[0]) for k, v in form.errors.items()]))

@staff_member_required
@csrf_exempt
def update_item_keywords(request):
    form = SearchForm(request.POST or None)
    if form.is_valid():
        # load custom words for jieba
        tags = StandardTag.objects.exclude(type='ignore').values_list('tag', flat=True)
        for t in tags:
            jieba.add_word(t, freq=50000)

        items_id = form.cleaned_data['q'].split(',')
        items = StoreItem.objects.filter(id__in=items_id)
        for item in items:
            p_item = preprocessing.models.Item(item.name)
            item.keywords = p_item.keywords
            item.save()
        return HttpResponse('done!')
    return HttpResponse(json.dumps([(k, v[0]) for k, v in form.errors.items()]))

@staff_member_required
@csrf_exempt
def search_items(request, template='standard/search_items_with_tags.html'):
    form = SearchForm(request.POST or None)
    items = []
    keywords = set()
    if form.is_valid():
        keywords = form.cleaned_data['q'].split(',')
        data = pandas.read_sql_query(
            '''
            SELECT
                items.id,
                items.name,
                items.keywords,
                stores.name as store_name
            FROM
                store_storeitem items,
                store_store stores
            WHERE
                items.store_id = stores.id AND
                items.keywords @> array[%(keywords)s];
            ''',
            params = {'keywords': keywords},
            con = connection)
        items = [row.to_dict() for _, row in data.iterrows()]
        print items
    return render(request, template, {'form': form, 'items': items, 'keywords': set(keywords)})


@staff_member_required
@csrf_exempt
def match_store_items(request, store_id, brand_tag_id, template='standard/match_store_items.html'):
    tag = StandardTag.objects.get(id=brand_tag_id)
    out = algorithms.match_items(store_id, tag.tag)
    accuracy = 0
    total = float(len(out))
    for k, val in out:
        if val['store_item']['barcode'] == val['standard_item']['barcode']:
            accuracy += 1
    return render(request, template, {'out': out, 'tag': tag, 'accuracy': round(accuracy / total * 100.0, 2), 'acc_raw': '%s/%s' % (accuracy, total)})

@staff_member_required
def map_store_category_to_standard_category(request, store_category_id, template='standard/map_store_category_to_standard_category.html'):
    choices = Category.objects.values('id', 'name', 'level')
    instance = StoreCategory.objects.get(id = store_category_id)
    form = StandardSeriesBatchUpdateForm(request.POST or None)
    msg = None
    if form.is_valid():
        category_id = form.cleaned_data['category_id']
        instance.std_category = Category.objects.get(pk=category_id)
        instance.operator = request.user
        instance.save()
        msg = u'更新成功'
    else:
        print form.errors

    return render(request, template, {'instance': instance, 'form': form, 'msg': msg, 'choices': choices})


