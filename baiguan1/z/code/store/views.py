# -*- coding: utf-8 -*-
from django.views.generic.base import View
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect

from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.utils import six
from django.views.decorators.http import require_GET
import third_party_db_helper
import pandas
import traceback

from standard.models import StandardItem, Category
from .models import (StoreItem, Store,
                     TransactionAccount,
                     StoreCategory,
                     ChainStore)
from .forms import MatchForm, SearchForm
from .custom_models import (DailyOnlineRank,
                            OverallOnlineRank,
                            WeeklyOnlineRank,
                            MonthlyOnlineRank)

import collections
import json
from .forms import StoreIdsForm, StoreShelfForm, ThirdPartyDBInfoForm
from math import ceil

from .forms import StoreDateRangePickerForm
from .forms import StoreDateRangePickerDetailForm
from .forms import StoreCategoryForm
from .forms import StoreIdForm
from .forms import TransactionWechatAccountForm, TransactionAlipayAccountForm, ThirdPartyDBInfo
import datetime
from django.db import connection
from core import sql_utils
from core import loss_analysis
from core.choices import STORE_WEEK
from core.store_nearby_analysis import get_store_nearby
from core.store_nearby_analysis import get_store_sales_category
from core.loss_analysis import median
from core.store_prices import get_prices_category
from core.store_basket import get_basket_coefficient
from core.store_basket import get_basket_week
from core.store_basket import get_basket_salesper
from core.choices import ENTITY_TYPE_CHOICES
from pairwise import Similarity, adjusted_cosine, get_expect_value, pearson_correlation, get_adjusted_cosine
from summary.models import DailyStoreSummary
from django.db.models import Avg
from transactions import AlipayHelper, WeChatPaymentHelper, WECHAT_DOWNLOAD_BILL_URl, gen_nonce_str, SERVICE_SINGLE_TRADE_QUERY
from math import radians, cos, sin, asin, sqrt, atan2

import redis
import os
import time
import math
import logging
logger = logging.getLogger(__name__)
# from .forms import ExtractItemMetaForm
# from preprocessing.utils import rank_standard_items, find_ranking_candidates

# from django.db import connection

@staff_member_required
def search_standard_items(request):
    form = SearchForm(request.GET or None)
    out = {'results': []}
    if form.is_valid():
        q = form.cleaned_data['q']
        out_list = list(StandardItem.objects.filter(name__icontains = q).order_by('-num_matches').values('name', 'id', 'num_matches'))[:10]
        for k in range(len(out_list)):
            out_list[k]['name'] = '%s (%s)' % (out_list[k]['name'], out_list[k]['num_matches'])
        out['results'] = out_list


    return HttpResponse(json.dumps(out), content_type="application/json")

@staff_member_required
def mark_status(request, item_pk, status):
    store_item = StoreItem.objects.get(pk=item_pk)
    store_item.status = status
    store_item.operator = request.user
    store_item.save()
    return redirect(request.GET.get('next'))


@staff_member_required
def matches(request, item_pk, template='store/matches.html'):
    form = MatchForm(request.POST or None)
    store_item = StoreItem.objects.get(pk=item_pk)
    if form.is_valid():
        store_item.standard_item = StandardItem.objects.get(pk=form.cleaned_data['matched_id'])
        store_item.operator = request.user
        store_item.status = 'human_verified'
        store_item.save()


    candidates_ids = store_item.candidates
    result = collections.OrderedDict()
    standard_item_in_candidates = False
    if candidates_ids:
        candidates_scores = store_item.candidates_scores
        candidates = StandardItem.objects.filter(id__in = candidates_ids).values('id', 'name', 'num_matches')
        for i in range(len(candidates_ids)):
            result[candidates_ids[i]] = {'score': round(candidates_scores[i] * 100.0, 2)}

        for c in candidates:
            result[c['id']]['name'] = c['name']
            result[c['id']]['num_matches'] = c['num_matches']

    if store_item.standard_item:
        standard_item = store_item.standard_item
        if candidates_ids and standard_item.id not in candidates_ids:
            standard_item_in_candidates = True
    else:
        standard_item = None

    return render(request, template, {'store_item': store_item, 'result': result, 'standard_item': standard_item, 'in_candidates': standard_item_in_candidates})

@staff_member_required
def store_sku_comparison(request, template='store/sku_comparison.html'):
    form = StoreIdsForm(request.GET or None)

    # key: device_id
    # value: store items
    store_items = {}

    # key: item_name
    # value: device_id
    # sort order by # of device_id
    result = {}
    stats = {}

    if form.is_valid():
        ids = form.cleaned_data['store_ids']
        id_toks = set(ids.split(','))

        for i in id_toks:
            store_items[i] = list(StoreItem.objects.filter(store__store_id=i).values('store', 'name', 'price'))

        for device_id, items in store_items.items():
            for item in items:
                if item['name'] not in result:
                    result[item['name']] = [device_id]
                else:
                    result[item['name']].append(device_id)

        for item, ids in result.items():
            if len(ids) not in stats:
                stats[len(ids)] = 1
            else:
                stats[len(ids)] += 1

        for key in stats.keys():
            stats[key] = {'per': round(stats[key]/float(len(result.keys())) * 100.0, 2),  'raw': stats[key]}
    else:
        print form.errors
    out_result = sorted(result.items(), key=lambda x: len(x[1]), reverse=True)

    return render(request, template, {'result': out_result, 'stats': stats, 'form': form})

@staff_member_required
def store_update_shelf(request, store_id, template='store/shelf_update.html'):
    store = Store.objects.get(pk=store_id)
    form = StoreShelfForm(request.POST or None, instance=store)

    if form.is_valid():
        instance = form.save(store=store)
    else:
        print form.errors
    return render(request, template, {'form': form, 'store_id': store_id})


@staff_member_required
def store_item_search(request, store_id):
    form = SearchForm(request.GET or None)
    out = {'results': []}
    if form.is_valid():
        q = form.cleaned_data['q']
        out_list = list(StoreItem.objects.filter(store__id=store_id, name__icontains = q).values('name', 'id', 'price'))
        for k in range(len(out_list)):
            out_list[k]['name'] = '%s (%s)' % (out_list[k]['name'], out_list[k]['price'])
        out['results'] = out_list

    return HttpResponse(json.dumps(out), content_type='application/json')

@login_required
def sample_items(request):
    all_items = StoreItem.objects.filter(store__id=4999)
    paginator = Paginator(all_items, 50)

    page = request.GET.get('p', 1)
    try:
        items = paginator.page(page).object_list
    except PageNotAnInteger:
        items = paginator.page(1).object_list
    except EmptyPage:
        items = paginator.page(paginator.num_pages).object_list
    out_item_list = list(items.values('name', 'price', 'image_url'))
    for i in range(len(out_item_list)):
        out_item_list[i]['score'] = (len(out_item_list) - i) / float(len(out_item_list)) * 100.0 + 0.12
    out = {'results': out_item_list,
           'next': int(page) + 1,
           'total': paginator.num_pages}
    return HttpResponse(json.dumps(out), content_type='application/json')


class OnlineItem(View):
    # TODO don't hardcode
    online_store_ids = [4995, 4999, 4996, 4998, 4993, 4994, 4991, 4997, 4992]
    online_chainstore_ids = [29, 30, 31]

    @staticmethod
    def get_leaf_cat(std_cat):
        result = []
        wait_for_visit = [int(std_cat)]
        while len(wait_for_visit) > 0:
            item = wait_for_visit.pop()
            result.append(item)
            children = [c.id for c in
                        Category.objects.filter(parent_id=item).all()]
            wait_for_visit.extend(children)
        return result

    @classmethod
    def get_store_cat_ids(cls, source, std_cat):
        # get the corresponding chainstore ids
        std_cat_ids = cls.get_leaf_cat(std_cat)
        if source:
            cs_ids = [i.id for i in ChainStore.objects.raw(
                "SELECT * FROM store_chainstore WHERE name=%s",
                [source])]
        else:
            cs_ids = cls.online_chainstore_ids
        # it should be free of injection here, as the cs_ids come from
        # internal sources
        return [sc.id for sc in StoreCategory.objects.filter(
            store_id__in=cs_ids, std_category_id__in=std_cat_ids).all()]

    @staticmethod
    def get_model_by_name(grandularity):
        if grandularity == 'daily':
            model = DailyOnlineRank
        elif grandularity == 'weekly':
            model = WeeklyOnlineRank
        elif grandularity == 'monthly':
            model = MonthlyOnlineRank
        else:
            model = OverallOnlineRank
        return model

    @staticmethod
    def paginate(model, query):
        page = query.pop('page', None)
        per_page = query.pop('per_page', None)
        if not page:
            page = 1
        else:
            page = int(page)

        if not per_page:
            per_page = 50
        else:
            per_page = int(per_page)
        count = model.get_count(query)
        page_num = int(ceil(count / float(per_page)))
        if page > page_num:
            page = page_num
        if page <= 0:
            raise Http404
        offset = (page - 1) * per_page
        query['offset'] = offset
        query['limit'] = per_page
        # (page_num, next page)
        return (page_num,
                page + 1 if page + 1 < page_num else page_num)

    def get(self, request, *args, **kwargs):
        querydict = request.GET
        query = {}
        for k, v in six.iteritems(querydict):
            if k == 's[]':
                query['s'] = querydict.getlist('s[]')
            else:
                query[k] = v
        grandularity = query.pop('grand', None)
        model = self.get_model_by_name(grandularity)
        logger.info('[OnlineItem] CustomModel with tablename '
                    + model._meta.table)
        # deal with category
        source = query.get('source', None)
        std_cat = query.pop('std_cat', None)
        if std_cat:
            store_cat_ids = self.get_store_cat_ids(source, std_cat)
            query['cat_type'] = store_cat_ids
            logger.info('Store categories: ' +
                        ','.join([str(sc) for sc in store_cat_ids]))
            if len(store_cat_ids) == 0:
                raise Http404
        page_num, next_p = self.paginate(model, query)
        logger.info('getting object with query:' + str(query))
        data = model.get_objects(query)
        for d in data:
            if pandas.isnull(d['price']):
                d['price'] = 0
            if pandas.isnull(d['store_id']):
                d['store_id'] = 0
        r = {'total': page_num, 'results': data, 'next': next_p}

        return JsonResponse(r)

def store_top_item_view(request, template='store/store_top_item.html'):

    form = StoreDateRangePickerForm(request.GET or None)
    if not form.is_valid():
        return HttpResponse('missing store_id')

    start_date = form.cleaned_data.get('start_date')
    if not start_date:
        start_date = (datetime.date.today() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
    end_date = form.cleaned_data.get('end_date')
    if not end_date:
        end_date = datetime.date.today().strftime('%Y-%m-%d')
    store_id = form.cleaned_data['store_id']

    sql = """
    SELECT
      sum(sd.num) as sum_num,
      sum(sd.sales) as sum_sales,
      sd.item_id as item_id,
      ss.name as name
    FROM
      summary_dailystoreitemsummary as sd,
      store_storeitem as ss
    WHERE
      sd.date BETWEEN to_date('%(start_date)s','YYYY-MM-DD') AND to_date('%(end_date)s','YYYY-MM-DD') AND
      sd.store_id = '%(store_id)s' AND
      sd.item_id = ss.id
    GROUP BY
      sd.item_id,
      ss.name
    ORDER BY
      sum_num desc limit 20;
    """ % {'start_date': start_date, 'end_date': end_date, 'store_id': store_id}

    cur = connection.cursor()
    cur.execute(sql)
    result = sql_utils.dictfetchall(cur)
    index = 0
    lose_count_all = 0
    for r in result:
        index+=1
        r['index'] = index
        if r['sum_num'] == 0:
            r['avg_price'] = round(0,5)
        else:
            r['avg_price'] = round(r['sum_sales']/r['sum_num'],5)
        item_id = r['item_id']
        lose_result = loss_analysis.loss_analysis(start_date,end_date,item_id)
        r['lose_count'] = lose_result['lose_count']
        if r['sum_sales'] == 0:
            r['lose_per'] = str(round(0,2))+'%'
        else:
            r['lose_per'] = str(round(r['lose_count']*100.0/r['sum_sales'],2))+'%'
        lose_count_all += lose_result['lose_count']

    days = (datetime.datetime.strptime(end_date, "%Y-%m-%d").date() - datetime.datetime.strptime(start_date, "%Y-%m-%d").date()).days
    return render(request, template, {'result': result,
                                      'store_id': store_id,
                                      'start_date': start_date,
                                      'end_date': end_date,
                                      'lose_count_all': lose_count_all,
                                      'days': days,
                                      })

def store_top_item_detail_view(request, template='store/store_top_item_detail.html'):

    form = StoreDateRangePickerDetailForm(request.GET or None)
    if not form.is_valid():
        return HttpResponse('missing item_id')

    start_date = form.cleaned_data.get('start_date')
    if not start_date:
        start_date = (datetime.date.today() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
    end_date = form.cleaned_data.get('end_date')
    if not end_date:
        end_date = datetime.date.today().strftime('%Y-%m-%d')
    item_id = form.cleaned_data['item_id']

    lose_result = loss_analysis.loss_analysis(start_date,end_date,item_id)
    result = lose_result['result']
    lose_days = lose_result['lose_days']
    lose_dates = lose_result['lose_dates']
    lose_count = lose_result['lose_count']
    medians = lose_result['medians']

    mapData = {
    "xAxis":{"data":[],'boundaryGap':False,"axisLabel":{"interval":0,"rotate":90,"textStyle":{"fontSize":10}}},
    "series":[{"name":u"本店销量","data":[],"type":"line"},{"name":u"历史销量","data":[],"type":"line",'lineStyle':{'normal':{'type':'dashed'}}}]
    }
    item_name = ""
    for r in result:
        if r["name"]:
            item_name = r["name"]
        date = r["date"]
        sales = r["sales"]
        if not sales:
            sales = 0
        if date in lose_dates:
            sales = {
            'value':sales,
            'symbol':'pin',
            'symbolSize':20,
                    }
        mapData['series'][0]["data"].append(sales)
        week = datetime.datetime.strptime(date, "%Y-%m-%d").weekday()
        mapData['series'][1]["data"].append(medians[week])
        mapData['xAxis']["data"].append(date+"("+STORE_WEEK[week]+")")


    return render(request, template, {'result': result,
                                      'lose_days':lose_days,
                                      'lose_dates':json.dumps(lose_dates),
                                      'lose_count':lose_count,
                                      'item_id': item_id,
                                      'start_date': start_date,
                                      'end_date': end_date,
                                      'mapData_series': json.dumps(mapData['series']),
                                      'mapData_xAxis': json.dumps(mapData['xAxis']),
                                      'item_name': json.dumps(item_name)
                                      })

def store_category_nearby_view(request, template='store/store_category_nearby.html'):
    form = StoreDateRangePickerForm(request.GET or None)
    if not form.is_valid():
        return HttpResponse('missing store_id')

    start_date = form.cleaned_data.get('start_date')
    if not start_date:
        start_date = (datetime.date.today() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
    end_date = form.cleaned_data.get('end_date')
    if not end_date:
        end_date = datetime.date.today().strftime('%Y-%m-%d')
    store_id = form.cleaned_data['store_id']

    stores_nearby = get_store_nearby(1000,store_id)

    nearby_sales = {}
    for store in stores_nearby:
        current_store_id = store['store_id']
        store_sales_category = get_store_sales_category(current_store_id,start_date,end_date)
        for sales_category in store_sales_category:
            sum_sales = sales_category['sum_sales']
            category = sales_category['category']
            if category not in nearby_sales:
                nearby_sales[category] = {'data':[]}
            nearby_sales[category]['data'].append(sum_sales)
    for category,detail in nearby_sales.items():
        medi = median(detail['data'])
        detail['median'] = medi

    my_store_sales_category = get_store_sales_category(store_id,start_date,end_date)

    xAxis = [{"type":"category","data":[],"axisLabel":{"interval":0,"rotate":25}}]
    series = [{'name':u'本店销量',"type":"bar","data":[]},
              {'name':u'周边销量',"type":"line","data":[],'itemStyle':{'normal':{'color':'#EE2C2C'}}}
             ]
    #markPoint = {'data':[],'itemStyle':{'normal':{'color':'#FF3030'}},'symbol':'roundRect','symbolSize':30}
    #index = 0
    for sale_category in my_store_sales_category:
        category = sale_category['category']
        sum_sales = sale_category['sum_sales']
        median_nearby_sum_sales = nearby_sales[category]['median']
        xAxis[0]['data'].append(category)
        series[0]["data"].append(sum_sales)
        series[1]["data"].append(median_nearby_sum_sales)
    #    data = {'coord':[index,median_nearby_sum_sales],'value':sum_sales/median_nearby_sum_sales}
    #    markPoint['data'].append(data)
    #    index += 1

    #series[0]['markPoint'] = markPoint
    return render(request, template, {
                                      'store_id': store_id,
                                      'start_date': start_date,
                                      'end_date': end_date,
                                      'xAxis': json.dumps(xAxis),
                                      'series': json.dumps(series),
                                      })

def store_prices_view(request, template='store/store_prices.html'):
    form = StoreCategoryForm(request.GET or None)
    if not form.is_valid():
        return HttpResponse('missing store_id')

    start_date = form.cleaned_data.get('start_date')
    if not start_date:
        start_date = (datetime.date.today() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
    end_date = form.cleaned_data.get('end_date')
    if not end_date:
        end_date = datetime.date.today().strftime('%Y-%m-%d')
    store_id = form.cleaned_data['store_id']
    category = form.cleaned_data['category']

    prices_category = get_prices_category(store_id,start_date,end_date)
    categorys = prices_category.keys()
    if categorys:
        if not category:
            category = categorys[0]
        if category in categorys:
            price_num = prices_category[category]
    else:
        price_num = {}
    xAxis = [{"type":"category","data":[],"axisLabel":{"interval":0,"formatter":'{value}元'},'name':u'价格'}]
    series = [
              {'name':u'数量',"type":"bar","data":[],'itemStyle':{'normal':{'color':'#C6E2FF'}}},
             ]
    for key,value in sorted(price_num.items(),key = lambda x:x[0]):
        xAxis[0]['data'].append(key)
        series[0]['data'].append(value)

    return render(request, template, {
                                      'store_id': store_id,
                                      'start_date': start_date,
                                      'end_date': end_date,
                                      'xAxis': json.dumps(xAxis),
                                      'series': json.dumps(series),
                                      'category': category,
                                      'categorys': categorys,
                                      })

def store_analysis_view(request, template='store/store_analysis.html'):
    form = StoreIdForm(request.GET or None)
    if not form.is_valid():
        return HttpResponse('missing store_id')

    store_id = form.cleaned_data['store_id']

    return render(request, template, {
                                      'store_id': store_id,
                                      })

def store_basket_quadrant_view(request, template='store/store_basket_quadrant.html'):
    form = StoreCategoryForm(request.GET or None)
    if not form.is_valid():
        return HttpResponse('missing store_id')

    start_date = form.cleaned_data.get('start_date')
    if not start_date:
        start_date = (datetime.date.today() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
    end_date = form.cleaned_data.get('end_date')
    if not end_date:
        end_date = datetime.date.today().strftime('%Y-%m-%d')
    store_id = form.cleaned_data['store_id']
    category = form.cleaned_data['category']
    results = get_basket_coefficient(store_id,start_date,end_date)
    basket_details = {}
    for result in results:
        current_category = result['category']
        if current_category not in basket_details:
            basket_details[current_category] = []
        detail = [result['basket'],result['count_id'],result['name'],result['sum_num'],result['price_avg'],result['sum_sales']]
        basket_details[current_category].append(detail)

    categorys = basket_details.keys()
    basket_detail = []
    basket_line = 0
    if categorys:
        if not category:
            category = categorys[0]
        if category in categorys:
            basket_detail = basket_details[category]
    else:
        basket_detail = []

    if len(basket_detail)>0:
        for data in basket_detail:
            basket_line += data[0]
        basket_line/=len(basket_detail)

    series = [
              {'name':u'count',"type":"scatter","data":basket_detail,'itemStyle':{'normal':{'color':'#C6E2FF'}},'markLine':{'data':[{'type':'average','name':u'平均值'},{'xAxis':basket_line}],}},
             ]

    return render(request, template, {
                                      'store_id': store_id,
                                      'start_date': start_date,
                                      'end_date': end_date,
                                      'series': json.dumps(series),
                                      'category': category,
                                      'categorys': categorys,
                                      })

def store_basket_category_view(request, template='store/store_basket_category.html'):
    form = StoreDateRangePickerForm(request.GET or None)
    if not form.is_valid():
        return HttpResponse('missing store_id')

    start_date = form.cleaned_data.get('start_date')
    if not start_date:
        start_date = (datetime.date.today() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
    end_date = form.cleaned_data.get('end_date')
    if not end_date:
        end_date = datetime.date.today().strftime('%Y-%m-%d')
    store_id = form.cleaned_data['store_id']

    results = get_basket_coefficient(store_id,start_date,end_date)
    series = []
    xAxis = []
    for result in results:
        basket = result['basket']
        xAxi = math.ceil(basket)
        if xAxi not in xAxis:
            xAxis.append(xAxi)
    xAxis = {'type':'category','data':sorted(xAxis),"axisLabel":{"interval":0,},'name':u'购物篮系数'}

    category_price_num = {}
    for result in results:
        category = result['category']
        if category not in category_price_num:
            category_price_num[category] = {}
            for price_level in xAxis['data']:
                category_price_num[category][price_level] = 0
        basket = math.ceil(result['basket'])
        category_price_num[category][basket] += 1

    for category,detail in category_price_num.items():
        items = sorted(detail.iteritems(),key = lambda x:x[0])
        data = []
        for item in items:
            data.append(item[1])
        series_one = {'name':category,'type':'bar','stack':'all','data':data}
        series.append(series_one)
    legend_data = category_price_num.keys()

    #购物篮系数百分比
    basket_num = {}
    for category,price_num in category_price_num.items():
        for price,num in price_num.items():
            if price not in basket_num:
                basket_num[price] = 0.0
            basket_num[price] += num
    basket_all = len(results)
    index = 0
    for price in xAxis['data']:
        basket_per = round(basket_num[price]/basket_all*100,2)
        xAxis['data'][index] = str(xAxis['data'][index])+'\n('+str(basket_per)+'%)'
        index += 1
    basket_num_list = sorted(basket_num.items(),key = lambda x:x[0])

    index_out=0
    for series_one in series:
        data = series_one['data']
        category = series_one['name']
        for index in range(len(data)):
            data_per = round(data[index]*1.0/basket_num_list[index][1]*100,2)
            data[index] = [xAxis['data'][index],data[index],'('+str(data_per)+'%)',category]
        series[index_out]['data'] = data
        index_out += 1


    return render(request, template, {
                                      'store_id': store_id,
                                      'start_date': start_date,
                                      'end_date': end_date,
                                      'series': json.dumps(series),
                                      'xAxis':json.dumps(xAxis),
                                      'legend_data':json.dumps(legend_data)
                                      })

def store_basket_week_view(request, template='store/store_basket_week.html'):
    form = StoreIdForm(request.GET or None)
    if not form.is_valid():
        return HttpResponse('missing store_id')

    store_id = form.cleaned_data['store_id']
    results = get_basket_week(store_id)
    stores_nearby = get_store_nearby(1000,store_id)
    stores_nearby_results = {}
    for store_nearby in stores_nearby:
        current_store_id = store_nearby['store_id']
        nearby_results = get_basket_week(current_store_id)
        for week,week_detail in nearby_results.items():
            if week not in stores_nearby_results:
                stores_nearby_results[week] = {'data':[],'basket':''}
            stores_nearby_results[week]['data'].append(week_detail['basket'])
    for week,week_detail in stores_nearby_results.items():
        medi = median(week_detail['data'])
        stores_nearby_results[week]['basket'] = medi

    xAxis = [{"type":"category","data":[],"axisLabel":{"interval":0}}]
    series = [{'name':u'购物篮系数',"type":"bar","data":[]},
              {'name':u'周边购物篮系数',"type":"line","data":[],'itemStyle':{'normal':{'color':'#EE2C2C'}}}
             ]
    for week in range(7):
        xAxis[0]['data'].append(STORE_WEEK[week])
        series[0]['data'].append(round(results[week]['basket'],5))
        series[1]['data'].append(round(stores_nearby_results[week]['basket'],5))

    return render(request, template, {
                                      'store_id': store_id,
                                      'series': json.dumps(series),
                                      'xAxis':json.dumps(xAxis),
                                      })
def store_basket_hour_view(request, template='store/store_basket_hour.html'):
    form = StoreBasketHourForm(request.GET or None)
    if not form.is_valid():
        return HttpResponse('missing store_id')

    store_id = form.cleaned_data['store_id']
    start_day = form.cleaned_data['start_day']
    end_day = form.cleaned_data['end_day']
    if not start_day:
        start_day = u'一'
    if not end_day:
        end_day = u'一'
    start_day = STORE_WEEK.index(start_day)
    end_day = STORE_WEEK.index(end_day)

    return render(request, template, {
                                      'store_id': store_id,
                                      'series': json.dumps(series),
                                      'xAxis':json.dumps(xAxis),
                                      })

def store_basket_sales_view(request, template='store/store_basket_sales.html'):
    form = StoreDateRangePickerForm(request.GET or None)
    if not form.is_valid():
        return HttpResponse('missing store_id')

    store_id = form.cleaned_data['store_id']
    start_date = form.cleaned_data.get('start_date')
    if not start_date:
        start_date = (datetime.date.today() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
    end_date = form.cleaned_data.get('end_date')
    if not end_date:
        end_date = datetime.date.today().strftime('%Y-%m-%d')
    results = get_basket_salesper(store_id,start_date,end_date)
    xAxis = [{"type":"category","data":[],"axisLabel":{"interval":0,"rotate":90,"textStyle":{"fontSize":10}}}]
    series = [{'name':u'销售占比',"type":"line","data":[]},
              {'name':u'购物篮系数',"type":"line","data":[],'itemStyle':{'normal':{'color':'#EE2C2C'}},'yAxisIndex':1}
             ]
    for result in results:
        series[0]['data'].append(round(result['sales_per']*100,2))
        series[1]['data'].append(round(result['basket'],2))
        out_date = result['out_date']
        week = datetime.datetime.strptime(out_date, "%Y-%m-%d").weekday()
        xAxis[0]['data'].append(out_date+"("+STORE_WEEK[week]+")")

    return render(request, template, {
                                      'store_id': store_id,
                                      'start_date': start_date,
                                      'end_date': end_date,
                                      'series': json.dumps(series),
                                      'xAxis':json.dumps(xAxis),
                                      })


@login_required(login_url='/login/')
def add_transaction_accounts(request, template='transactions/transaction.html'):
    if request.method == 'GET':
        data = {}
        info = TransactionAccount.objects.filter(user=request.user)
        if info.count() != 0:
            info = info[0]
            if info.wechat_mch_id and info.wechat_api_key and info.wechat_password and info.wechat_username and info.wechat_appid:
                data['wechat'] = True
            if info.alipay_pid and info.alipay_appid and info.alipay_key:
                data['alipay'] = True
        if data.get('wechat') and data.get('alipay'):
            return HttpResponseRedirect('/integration/navigation')
        return render(request, template, data)
    else:
        response = {'success': 0, 'error': ''}
        if request.POST.get('platform') == 'wechat':
            form = TransactionWechatAccountForm(request.POST or None)
            if not form.is_valid():
                response['error'] = u'必填字段未填写。'
                return HttpResponse(json.dumps(response), content_type="application/json")
            mch_id = form.cleaned_data.get('mch_id')
            appid = form.cleaned_data.get('appid')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            api_key = form.cleaned_data.get('api_key')
            content = WeChatPaymentHelper.access_url(WECHAT_DOWNLOAD_BILL_URl, key=api_key, appid=appid, mch_id=mch_id, bill_date='20161210', nonce_str=gen_nonce_str(), bill_type='ALL')
            print content
            if content.get('xml').get('return_msg') == 'No Bill Exist' or content.get('xml').get('return_msg') == 'invalid bill_date' or content.get('xml').get('return_code') != 'FAIL':
                info = TransactionAccount.objects.filter(user=request.user)
                if info.count()==0:
                    info = TransactionAccount(user=request.user, wechat_mch_id=mch_id, wechat_username=username, wechat_password=password, wechat_appid=appid, wechat_api_key=api_key)
                    info.save()
                else:
                    info = info[0]
                    info.wechat_mch_id = mch_id
                    info.wechat_username = username
                    info.wechat_password = password
                    info.wechat_appid = appid
                    info.wechat_api_key = api_key
                    info.save()
                response['success'] = 1
        elif request.POST.get('platform') == 'alipay':
            form = TransactionAlipayAccountForm(request.POST or None)
            if not form.is_valid():
                response['error'] = u'必填字段未填写。'
                return HttpResponse(json.dumps(response), content_type="application/json")
            appid = form.cleaned_data.get('appid')
            pid = form.cleaned_data.get('pid')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            key = form.cleaned_data.get('key')
            info = TransactionAccount.objects.filter(user=request.user)
            content = AlipayHelper.access_service('account.page.query', key=key, _input_charset='utf-8',partner=pid, page_no=1)
            print content
            if content.get('alipay').get('error') == 'REQUIRED_DATE':
                if info.count()==0:
                        info = TransactionAccount(user=request.user, alipay_username=username, alipay_password=password, alipay_pid=pid, alipay_appid=appid, alipay_key=key)
                        info.save()
                else:
                    info = info[0]
                    info.alipay_username = username
                    info.alipay_password = password
                    info.alipay_appid = appid
                    info.alipay_key = key
                    info.alipay_pid = pid
                    info.save()
                response['success'] = 1
        return HttpResponse(json.dumps(response), content_type="application/json")

@login_required(login_url='/login/')
def navigation(request, template='navigation.html'):
    data = {}
    db_info = ThirdPartyDBInfo.objects.filter(user=request.user)
    info = TransactionAccount.objects.filter(user=request.user)
    if db_info.count() != 0:
        db_info = db_info[0]
        print db_info.dbtype, db_info.dbhost, db_info.dbpassword
        if db_info.dbtype is not None and db_info.dbhost and db_info.dbpassword:
            data['sql'] = True
    if info.count() != 0:
        info = info[0]
        if info.wechat_appid and info.wechat_api_key and info.wechat_mch_id:
            data['wechat'] = True
        if info.alipay_key and info.alipay_pid:
            data['alipay'] = True
    return render(request, template, data)

def haversine(lat1, lng1, lat2, lng2): # 经度1，纬度1，经度2，纬度2 （十进制度数）
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # 将十进制度数转化为弧度
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])

    # haversine公式
    dlng = lng2 - lng1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371.004 # 地球平均半径
    return c * r * 1000

x_pi = 3.14159265358979324 * 3000.0 / 180.0

def convert_gcj02_to_bd09(lat, lng):
    x = lng
    y = lat
    z = sqrt(x * x + y * y) + 0.00002 * sin(y * x_pi)
    theta = atan2(y ,x) + 0.000003 * cos(x * x_pi)
    lat = z * sin(theta) + 0.006
    lng = z * cos(theta) + 0.0065
    return lat, lng

def convert_bd09_to_gcj02(lat, lng):
    x = lng - 0.0065
    y = lat - 0.006
    z = sqrt(x * x + y * y) - 0.00002 * sin(y * x_pi)
    theta = atan2(y ,x) - 0.000003 * cos(x * x_pi)
    lat = z * sin(theta)
    lng = z * cos(theta)
    return lat, lng


redisC = redis.Redis(host=os.environ.get('CM_REDIS_URL'), port=os.environ.get('CM_REDIS_PORT'), password=os.environ.get('CM_REDIS_PASSWORD'), db=4)
# redisC = redis.Redis(host='172.31.15.191', port=6379, password='jhUasISA9qw12aSnaSd', db=4)

def store_comparison(request, stores, template='store/store_comparision.html'):

    stores = Store.objects.filter(id__in=set(stores.split('-')))
    all_stores = set()
    [all_stores.add(summary.store) for summary in DailyStoreSummary.objects.all()]
    store_vectors = [{'store_id':store.id, 'store_name': store.name, 'district':int(store.city_path.split('>')[-1]), 'vector': [redisC.scard('%s:%s' % (store.id, keyword)) for keyword, _type in ENTITY_TYPE_CHOICES]} for store in all_stores]
    vectors_dict = {}
    result = {}
    result['stores'] = []
    for store in stores:
        vectors_dict[store.id] = []
        summaries = DailyStoreSummary.objects.filter(store=store).values('store_id').annotate(avg_sales = Avg('sales'))
        for index in range(0, len(ENTITY_TYPE_CHOICES)):
            keyword, _type = ENTITY_TYPE_CHOICES[index]
            vectors_dict[store.id].append(redisC.scard('%s:%s' % (store.id, keyword)))
        _store_dict = {'id':store.id,'name': store.name, 'avg_sales':summaries[0]['avg_sales'], 'vector':vectors_dict[store.id], 'sims':[]}
        for _store in store_vectors:
            if _store.get('store_id') == store.id:
                continue
            _vector = _store.get('vector')
            _adjusted_cosine_result, _x_positive_num, _y_positive_num, _x_negative_num, _y_negative_num = get_adjusted_cosine(vectors_dict.get(store.id), _vector)
            if _adjusted_cosine_result>0.6:
                _store['adjusted_cosine'] = _adjusted_cosine_result
                _store['positive_num'] = _y_positive_num
                _store['negative_num'] = _y_negative_num
                _store['difference'] = (_y_positive_num - _y_negative_num) - (_x_positive_num - _x_negative_num)
                _store['min_predict_sales'] = summaries[0]['avg_sales'] * (float(_y_positive_num - _y_negative_num) / float(_x_positive_num - _x_negative_num))
                _store['max_predict_sales'] = summaries[0]['avg_sales'] * (float(_y_positive_num - _y_negative_num) / float(_x_positive_num - _x_negative_num))
                # _store['pgdp'] = CITY_INFO.get(City.objects.get(pk=_store.get('district')).id).get('pgdp')
                _store['sales'] = DailyStoreSummary.objects.filter(store__id=_store.get('store_id')).values('store_id').annotate(avg_sales = Avg('sales'))[0]['avg_sales']
                _store_dict['sims'].append(_store)
        result['stores'].append(_store_dict)

    adjusted_cosine_result, x_positive_num, y_positive_num, x_negative_num, y_negative_num = get_adjusted_cosine(vectors_dict.get(vectors_dict.keys()[0]), vectors_dict.get(vectors_dict.keys()[1]))
    sim = Similarity(vectors_dict.get(vectors_dict.keys()[0]), vectors_dict.get(vectors_dict.keys()[1]))
    result['euclidean_distance'] = sim.euclidean_distance()
    result['manhattan_distance'] = sim.manhattan_distance()
    result['cosine_similarity'] = sim.cosine_similarity()
    result['pearson_correlation'] = pearson_correlation([vectors_dict.get(vectors_dict.keys()[0])], [vectors_dict.get(vectors_dict.keys()[1])])[0][0]
    result['adjusted_cosine'] = adjusted_cosine_result
    result['positive_nums'] = [{'id':vectors_dict.keys()[0], 'positive_num': x_positive_num}, {'id':vectors_dict.keys()[1], 'positive_num': y_positive_num}]
    result['negative_nums'] = [{'id':vectors_dict.keys()[0], 'negative_num': x_negative_num}, {'id':vectors_dict.keys()[1], 'negative_num': y_negative_num}]
    result['difference'] = (x_positive_num - x_negative_num) - (y_positive_num - y_negative_num)
    return render(request, template, result)

@require_GET
@login_required(login_url='/login/')
def third_party_db_info_page(request, template='store/third_party_db.html'):
    return render(request, template)


class ThirdPartyDBAPI(View):
    def post(self, request, *args, **kwargs):
        """
        Return
        code 0: OK
        code 1: form validation error
        code 2: db fail to create db engine
        code 3: fetch table name erorr
        """
        form = ThirdPartyDBInfoForm(data=request.POST or None,
                                    request=request)
        if form.is_valid():
            dbtype = form.cleaned_data['dbtype']
            dbname = form.cleaned_data['dbname']
            dbhost = form.cleaned_data['dbhost']
            dbuser = form.cleaned_data['dbuser']
            dbpassword = form.cleaned_data['dbpassword']
            dbport = form.cleaned_data['dbport']
            if not dbname:
                dbname = ''
            if not dbport:
                dbport = '1521'
            try:
                db_helper = third_party_db_helper.get_db_helper_by_type(
                    dbtype,
                    dbhost,
                    dbuser,
                    dbpassword,
                    dbname,
                    dbport)
            except Exception as e:
                traceback.print_exec()
                return JsonResponse({
                    'code': 2,
                    'message': 'Failed to create db engine',
                    'errors': e.message
                })
            logger.info('DBURL: ' + db_helper.db_url)
            try:
                table_names = db_helper.get_user_table_names()
                instance = form.save()
                permissions = db_helper.verify_permissions()
                permission_code = ''.join([str(p['code']) for p in permissions])
                return JsonResponse({
                    'code': 0,
                    'data': {
                        'dbinfo': instance.to_dict(),
                        'table_names': table_names,
                        'permission_code': permission_code
                    }
                })
            except Exception as e:
                logger.error(e, 'Error occurred')
                return JsonResponse(
                    {'code': 3, 'message': 'DB connection error',
                     'errors': e.message})

        else:
            return JsonResponse(
                {'code': 1, 'message': 'form validation failed',
                 'errors': [k + ': ' + ','.join(v)
                            for k, v in form.errors.items()]})
