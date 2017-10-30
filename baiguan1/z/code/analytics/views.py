
# -*- coding: utf-8 -*-

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connection
import pandas
import datetime
import collections
from .forms import DateRangePickerForm
from store.models import City, StoreTag, ChainStore, StoreCategory, Store, StoreDailyTarget, Attribute, AttributeMap, StoreItemState, StoreItem, StoreItemInventory, ChainStoreItemInventory, StoreUser, UAC
from summary.models import DailyStoreItemSummary, DailyStoreSummary, DailyStoreCategorySummary
from standard.models import Category, StandardSeries, StandardItem, StandardTag
from user.models import CMUser
from page import Pagination
import json
from os import environ
import redis



TODAY = 0
YESTERDAY = 1
WEEKLY = 2
MONTHLY = 3
SEASONALLY = 4
YEARLY = 5



redisC = redis.Redis(host=environ.get('CM_REDIS_URL', ''), port=environ.get('CM_REDIS_PORT', ''),
                     password=environ.get('CM_REDIS_PASSWORD', ''), db=7)

def _get_store_tags(store_ids):
    tags_query = pandas.read_sql_query(
        '''
        SELECT
            id, tag, type
        FROM
            standard_standardtag
        WHERE
            tag = ANY (
                SELECT
                    keyword
                FROM (
                    SELECT
                        unnest(keywords) as keyword
                    FROM
                        store_storeitem
                    WHERE
                        array[store_id] <@ (%(store_ids)s)
                    GROUP BY
                        keyword
                )t
            );
        ''',
        params = {'store_ids': store_ids},
        con = connection)
    d = {}
    for _, row in tags_query.iterrows():
        row_dict = row.to_dict()
        d[row_dict['tag']] = {'id': row_dict['id'], 'type': row_dict['type']}
    return d

def _get_store_name(store_id):
    store_query = pandas.read_sql_query(
        '''
        SELECT
            name
        FROM
            store_store
        WHERE
            id = %(store_id)s
        ''',
        params = {'store_id': store_id},
        con = connection)
    return store_query['name'][0]

def _get_store_top_items(store_id):
    start_date = (datetime.date.today() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
    end_date = datetime.date.today().strftime('%Y-%m-%d')

    data = pandas.read_sql_query(
        sql = '''
            SELECT
                item_id,
                sum(summary.sales) as sales,
                ssi.name,
                ssi.keywords
            FROM
                summary_dailystoreitemsummary summary,
                store_storeitem ssi
            WHERE
                summary.store_id = %(store_id)s AND
                summary.date >= %(start_date)s AND summary.date <= %(end_date)s AND
                ssi.id = summary.item_id
            GROUP BY item_id, ssi.name, ssi.keywords
            ORDER BY sales DESC
            LIMIT 200;
        ''',
        params = {'start_date': start_date, 'end_date': end_date, 'store_id': store_id},
        con = connection)
    return [row.to_dict() for _, row in data.iterrows()]

def _get_store_brands_stats(store_ids, brand_name):
    tags = _get_store_tags(store_ids)
    items_query = pandas.read_sql_query(
        '''
        SELECT
            item.name, store.name as store_name, item.price, item.keywords
        FROM
            store_storeitem item, store_store store
        WHERE
            array[item.store_id] <@ (%(store_ids)s) AND
            item.store_id = store.id AND
            item.keywords @> array[%(brand_name)s]
        ORDER BY item.price;
        ''',
        params = {'store_ids': store_ids, 'brand_name': brand_name},
        con = connection)

    series = {u'#沒有系列': []}
    property_counts = collections.defaultdict(int)
    quantity_counts = collections.defaultdict(int)
    category_counts = collections.defaultdict(int)
    for _, row in items_query.iterrows():
        row_dict = row.to_dict()
        row_dict['tags'] = []
        no_series = True
        for k in row_dict['keywords']:
            if k in tags:
                row_dict['tags'].append({'tag': k, 'type': tags[k]['type']})
                if tags[k]['type'] == 'series':
                    no_series = False
                    if k not in series:
                        series[k] = []
                    series[k].append(row_dict)

                elif tags[k]['type'] == 'property':
                    property_counts[k] += 1
                elif tags[k]['type'] == 'quantity':
                    quantity_counts[k] += 1
                elif tags[k]['type'] == 'category':
                    category_counts[k] += 1
            else:
                row_dict['tags'].append({'tag': k, 'type': None})
        if no_series:
            series[u'#沒有系列'].append(row_dict)
    out_series = sorted(series.iteritems(), key=lambda (k, v): len(v), reverse=True)
    return {'num_sku': len(items_query),
            'property_counts': property_counts,
            'quantity_counts': quantity_counts,
            'category_counts': category_counts,
            'series': out_series}

@staff_member_required
def store_items_analytics(request, store_id, template='analytics/store_items_analytics.html'):
    form = DateRangePickerForm(request.POST or None)
    # if not form.is_valid():
    #     return HttpResponse('invalid date range')

    # start_date = form.cleaned_data.get('start_date')
    # if not start_date:
    start_date = (datetime.date.today() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
    # end_date = form.cleaned_data.get('end_date')
    # if not end_date:
    end_date = datetime.date.today().strftime('%Y-%m-%d')

    store_name = _get_store_name(store_id)

    total_sales_query = pandas.read_sql_query(
        '''
        SELECT
            sum(summary.sales) as sum
        FROM
            summary_dailystoreitemsummary summary
        WHERE
            summary.store_id = %(store_id)s AND
            summary.date >= %(start_date)s AND summary.date <= %(end_date)s
        ''',
        params = {'start_date': start_date, 'end_date': end_date, 'store_id': store_id},
        con = connection)
    total_sales = total_sales_query['sum'][0]

    tags = _get_store_tags([int(store_id)])

    data = pandas.read_sql_query(
        sql = '''
            SELECT
                item_id,
                sum(summary.sales) as sales,
                ssi.name,
                ssi.keywords
            FROM
                summary_dailystoreitemsummary summary,
                store_storeitem ssi
            WHERE
                summary.store_id = %(store_id)s AND
                summary.date >= %(start_date)s AND summary.date <= %(end_date)s AND
                ssi.id = summary.item_id
            GROUP BY item_id, ssi.name, ssi.keywords
            ORDER BY sales DESC
            LIMIT 200;
        ''',
        params = {'start_date': start_date, 'end_date': end_date, 'store_id': store_id},
        con = connection)

    ranked_items = []
    items_sales = {}
    for _, row in data.iterrows():
        row_dict = row.to_dict()
        ranked_items.append(row_dict)
        items_sales[row_dict['name']] = row_dict['sales']

    d = {}
    for ri in ranked_items:
        if not ri['keywords']:
            print 'skipping ', ri['name'], ' because empty keywords'
            continue

        ri['tags'] = []
        for k in ri['keywords']:
            if k in tags:
                ri['tags'].append({'tag': k, 'type': tags[k]['type']})
            else:
                ri['tags'].append({'tag': k, 'type': None})

        for k in ri['keywords']:
            if k in tags and tags[k]['type'] == 'brand':
                if k not in d:
                    d[k] = {'sales': 0, 'items': []}
                d[k]['sales'] += ri['sales']
                d[k]['items'].append(ri['name'])
                break



    run_sum = 0
    for k, v in d.items():
        run_sum += d[k]['sales']
        d[k]['per'] = float(d[k]['sales']) / total_sales * 100.0
        d[k]['brand_id'] = tags[k]['id']
        for i in range(len(d[k]['items'])):
            item_name = d[k]['items'][i]
            d[k]['items'][i] = {'name': item_name, 'per': float(items_sales[item_name]) / d[k]['sales'] * 100.0}

    ranked_brands = sorted(d.iteritems(),key=lambda (k,v): v['sales'],reverse=True)
    return render(request, template, {'ranked_items': ranked_items,
                                      'ranked_brands': ranked_brands,
                                      'total_sales': total_sales,
                                      'run_sum': round(float(run_sum) / total_sales * 100.0, 2),
                                      'store_name': store_name,
                                      'store_id': store_id})

WEB_STORE_IDS = [4991, 4992, 4993, 4994, 4995, 4996, 4997, 4998, 4999]
@staff_member_required
def store_brands_analytics(request, store_id, brand_tag_id, template='analytics/store_brands_analytics.html'):
    brand_query = pandas.read_sql_query('SELECT tag FROM standard_standardtag WHERE id=%(tag_id)s AND type=%(tag_type)s',
                                      params = {'tag_id': brand_tag_id, 'tag_type': 'brand'},
                                      con = connection)

    brand_name = brand_query['tag'][0]
    store_stats = _get_store_brands_stats([int(store_id)], brand_name)
    # std_stats = _get_store_brands_stats([], brand_name)
    return render(request, template, {'store_stats': store_stats,
                                      # 'std_stats': std_stats,
                                      'store_name': _get_store_name(store_id),
                                      'brand_name': brand_name})

def web_store_brands_analytics(request, brand_tag_id, template='analytics/store_brands_analytics.html'):
    brand_query = pandas.read_sql_query('SELECT tag FROM standard_standardtag WHERE id=%(tag_id)s AND type=%(tag_type)s',
                                      params = {'tag_id': brand_tag_id, 'tag_type': 'brand'},
                                      con = connection)

    brand_name = brand_query['tag'][0]
    store_stats = _get_store_brands_stats(WEB_STORE_IDS, brand_name)
    return render(request, template, {'store_stats': store_stats,
                                      'brand_name': brand_name})

def _get_brands(tags, ranked_items):
    d = {}
    for ri in ranked_items:
        if not ri['keywords']:
            print 'skipping ', ri['name'], ' because empty keywords'
            continue

        ri['tags'] = []
        for k in ri['keywords']:
            if k in tags:
                ri['tags'].append({'tag': k, 'type': tags[k]['type']})
            else:
                ri['tags'].append({'tag': k, 'type': None})

        for k in ri['keywords']:
            if k in tags and tags[k]['type'] == 'brand':
                if k not in d:
                    d[k] = {'sales': 0, 'items': []}
                d[k]['sales'] += ri['sales']
                d[k]['items'].append(ri['name'])
                break
    # ranked_brands = sorted(d.iteritems(),key=lambda (k,v): v['sales'],reverse=True)
    return d

@staff_member_required
def stores_stores_compare(request, template='analytics/stores_stores_compare.html'):
    form_store_id = request.GET.get('from_store', None)
    to_store_ids = request.GET.getlist('to_stores', None)
    print to_store_ids
    if not form_store_id or not to_store_ids:
        return HttpResponse('invalid from_store or to_stores')

    from_store_tags = _get_store_tags([int(form_store_id)])
    from_store_ranked_items = _get_store_top_items(form_store_id)
    from_store_brands  = set()
    for tag, t in from_store_tags.items():
        if t['type'] == 'brand':
            from_store_brands.add(tag)

    # to_store_tags = {}
    # to_store_items = {}
    to_store_brands = {}
    for t in to_store_ids:
        tags = _get_store_tags([int(t)])
        items = _get_store_top_items(t)
        to_store_brands[t] = _get_brands(tags, items)


    inner_brands = set()
    outter_brands = set()

    for store_id, brands in to_store_brands.items():
        inner_brands |= set(brands.keys()) & from_store_brands
        outter_brands |= set(brands.keys()) - from_store_brands

    return render(request, template, {'inner_brands': inner_brands,
                                      'outter_brands': outter_brands})

def current_week():
    current_week_day = datetime.datetime.now().weekday()
    start_date = (datetime.date.today() - datetime.timedelta(days=(current_week_day))).strftime('%Y-%m-%d')
    end_date = datetime.date.today().strftime('%Y-%m-%d')
    day_list = []
    total_day_list=[]
    for i in xrange(current_week_day, -1, -1):
        day_list.append((datetime.date.today() - datetime.timedelta(days = i)).strftime('%Y-%m-%d').split('-')[2])
        total_day_list.append((datetime.date.today() - datetime.timedelta(days = i)).strftime('%Y-%m-%d'))

    return start_date, end_date, day_list,total_day_list

def last_week():
    current_week_day = datetime.datetime.now().weekday()
    start_date =  (datetime.date.today() - datetime.timedelta(days=(current_week_day + 7))).strftime('%Y-%m-%d')
    end_date =  (datetime.date.today() - datetime.timedelta(days=current_week_day)).strftime('%Y-%m-%d')
    return start_date, end_date

def current_month():
    year, month, day = datetime.date.today().strftime('%Y-%m-%d').split('-')
    day = int(day)
    start_date = (datetime.date.today() - datetime.timedelta(days=(day-1))).strftime('%Y-%m-%d')
    end_date = datetime.date.today().strftime('%Y-%m-%d')
    day_list = []
    for i in xrange(day,0,-1):
        day_list.append((datetime.date.today() - datetime.timedelta(days = (i - 1))).strftime('%Y-%m-%d').split('-')[2])
    return start_date, end_date, day_list

def last_month():
    year, month, day = datetime.date.today().strftime('%Y-%m-%d').split('-')
    month = int(month)
    year = int(year)
    if month == 1:
        month = 13
    month = str(month - 1)
    year = str(year - 1)

    start_date = year + '-' + month + '-01'
    end_date = year + '-' + month + '-31'
    return start_date, end_date

def current_quarter():
    year, month, day=datetime.date.today().strftime('%Y-%m-%d').split('-')
    month = int(month)
    month_list = []
    if month in [1, 2, 3]:
        start_date = year + '-01-01'
        end_date = year + '-03-31'
        for i in xrange(month):
            month_list.append(i + 1)
    elif month in [4, 5, 6]:
        start_date = year + '-04-01'
        end_date = year + '-06-30'
        for i in xrange(month - 3):
            month_list.append(i + 4)
    elif month in [7, 8, 9]:
        start_date = year + '-07-01'
        end_date = year + '-09-30'
        for i in xrange(month - 6):
            month_list.append(i + 7)
    else:
        start_date = year + '-10-01'
        end_date = year + '-12-31'
        for i in xrange(month - 9):
            month_list.append(i + 10)
    return start_date, end_date, month_list

def current_year():
    year, month, day = datetime.date.today().strftime('%Y-%m-%d').split('-')
    start_date = year + '-01-01'
    end_date = year + '-12-31'
    month_list = []
    month = int(month)
    for i in xrange(month):
        month_list.append(i + 1)

    return start_date,end_date,month_list

def get_total_sales_by_days(start_date, end_date, chainstore_id):
    data = pandas.read_sql_query(
        sql = '''
            SELECT
                sum(summary.sales)-sum(target.sales)  as balance,
                sum(summary.sales)/sum(target.sales) as finsh_rate,
                round(cast (sum(target.sales)as numeric ), 2) as tsales,
                round(cast (sum(summary.sales)as numeric ), 2) as sales,
                round(cast (sum(summary.num) as numeric ), 2) as num_trades,
                round(cast (sum(summary.sales) / sum(summary.num) as numeric ), 2) as each_num_trades_sales
            FROM
                summary_dailystoreitemsummary summary
            LEFT JOIN
                store_store ssi
            ON
                (ssi.store_id = summary.store_id)
            LEFT JOIN
                store_storedailytarget target
            ON
                (ssi.id = target.store_id)
            WHERE
                ssi.chainstore_id = %(chainstore_id)s AND
                summary.date >= %(start_date)s AND summary.date <= %(end_date)s 
        ''',
        params = {'start_date': start_date, 'end_date': end_date, 'chainstore_id':chainstore_id},
        con = connection)
    return [row.to_dict() for _, row in data.iterrows()]   

def get_each_day_sales_by_week_or_by_month(start_date, end_date, chainstore_id):
    data = pandas.read_sql_query(
        sql = '''
            SELECT
                to_char(summary.date, 'YYYY-MM-DD') as d,
                round(cast (sum(summary.sales) as numeric ), 2) as sales,
                round(cast (sum(summary.num) as numeric ), 2) as num_trades,
                round(cast (sum(summary.sales) / sum(summary.num) as numeric ), 2) as each_num_trades_sales
            FROM
                summary_dailystoreitemsummary summary
            LEFT JOIN
                store_store ssi
            ON
                (ssi.store_id = summary.store_id)
            WHERE
                ssi.chainstore_id = %(chainstore_id)s AND
                summary.date >= %(start_date)s AND summary.date <= %(end_date)s 
            GROUP BY d
        ''',
        params = {'start_date': start_date, 'end_date': end_date,'chainstore_id':chainstore_id},
        con = connection)
    return [row.to_dict() for _, row in data.iterrows()]

def get_each_month_sales_by_year_or_by_quarter(start_date,end_date,chainstore_id):
    year, month, day = datetime.date.today().strftime('%Y-%m-%d').split('-')
    month = int(month)
    start_date_list = [year + '-01-01', year + '-02-01', year + '-03-01', year + '-04-01', year + '-05-01', year + '-06-01', year + '-07-01', year + '-08-01', year + '-09-01', year + '-10-01', year + '-11-01', year + '-12-01']
    
    data = pandas.read_sql_query(
        sql = '''
            SELECT
                to_char(summary.date, 'YYYY-MM') as d,
                round(cast (sum(summary.sales) as numeric ), 2) as sales,
                round(cast (sum(summary.num) as numeric ), 2) as num_trades,
                round(cast (sum(summary.sales) / sum(summary.num) as numeric ), 2) as each_num_trades_sales
            FROM
                summary_dailystoreitemsummary summary
            LEFT JOIN
                store_store ssi
            ON
                (ssi.store_id = summary.store_id)
            WHERE
                ssi.chainstore_id = %(chainstore_id)s AND
                summary.date >= %(start_date)s AND summary.date <= %(end_date)s 
            GROUP BY d
        ''',
        params = {'start_date': start_date, 'end_date': end_date, 'chainstore_id':chainstore_id},
        con = connection)
    return [row.to_dict() for _, row in data.iterrows()]
#参考函数_get_store_top_items
def rule_get_store_top_items(store_id, days=30, rule1='sales', rule2='DESC'):
    start_date = (datetime.date.today() - datetime.timedelta(days = days)).strftime('%Y-%m-%d')
    end_date = datetime.date.today().strftime('%Y-%m-%d')

    data = pandas.read_sql_query(
        sql = '''
            SELECT
                item_id,
                sum(summary.sales) as sales,
                sum(summary.num) as num,
                ssi.name,
                summary.barcode as barcode,
                state.name as status,
                round(cast (sum(summary.num) / %(days)s as numeric ), 2)  as eachday_num,
                summary.sales  as  each_sales
            FROM
                summary_dailystoreitemsummary summary,
                store_storeitem ssi,
                store_StoreItemState state

            WHERE
                summary.store_id = %(store_id)s AND
                summary.date >= %(start_date)s AND summary.date <= %(end_date)s AND
                ssi.id = summary.item_id AND
                ssi.item_state_id=state.id
            GROUP BY item_id, ssi.name, summary.barcode, state.name, summary.sales
            ORDER BY ''' + rule1 + ' ' + rule2 +
            '''
            LIMIT 200;
        ''',
        params = {'start_date': start_date, 'end_date': end_date, 'store_id': store_id, 'days':days},
        con = connection)
    return [row.to_dict() for _, row in data.iterrows()]

def num_to_chinese(num):
    to_dict={
    1:u'一', 2:u'二', 3:u'三', 4:u'四', 5:u'五', 6:u'六', 7:u'七', 8:u'八', 9:u'九', 10:u'十',
    11:u'十一', 12:u'十二', 13:u'十三', 14:u'十四', 15:u'十五', 16:u'十六', 17:u'十七', 18:u'十八', 19:u'十九', 20:u'二十',
    21:u'二十一', 22:u'二十二', 23:u'二十三', 24:u'二十四', 25:u'二十五', 26:u'二十六', 27:u'二十七', 28:u'二十八', 29:u'二十九', 30:u'三十',
    }
    
    return u'第' + to_dict[num] + u'页'

def get_city2_by_id(city_id):
    store_query = pandas.read_sql_query(
        '''
        SELECT
            name
        FROM
            store_city
        WHERE
            id = %(city_id)s
        ''',
        params = {'city_id': city_id},
        con = connection)
    return store_query['name'][0]

@login_required(login_url='/login/')
def get_storelist(request):
    # user = request.user
    # chainstore_id=StoreUser.objects.filter(user__username=user).values('permission__chain_store_permission').first()['permission__chain_store_permission']
    chainstore_id=32
    current_page = request.GET.get('current_page',1)
    all_response_date = {}
    date_rule = request.GET.get('date_rule', '1')
    if date_rule in ['1', '2', '3', '4']:
        if date_rule =='1':#today
            start_date =  datetime.date.today().strftime('%Y-%m-%d')
            end_date = datetime.date.today().strftime('%Y-%m-%d')
            day1, day2, day3, day4 = range_date(1)
        elif date_rule == '2':#current_week
            start_date, end_date, day_list,total_day_list = current_week()
            day1, day2, day3, day4 = week_date()
        elif date_rule == '3':#current_month
            start_date, end_date, day_list = current_month()
            day1, day2, day3, day4 = month_date()
        elif date_rule == '4':
            year, month, day = datetime.date.today().strftime('%Y-%m-%d').split('-')
            start_date = year + '-01-01'
            end_date=year + '-12-31'
            day1, day2, day3, day4 = year_date()

    keywords = request.GET.get('keywords', '')
    if keywords:
        current_store_list = search_storelist_by_sql(start_date, end_date, keywords)
    else:
        current_store_list = get_storelist_by_sql(start_date, end_date, chainstore_id)
    sales_growth_list = get_store_sales_increase(day1, day2, day3, day4, chainstore_id)

    for item in current_store_list:
        for item1 in sales_growth_list:
           if item['store_id'] == item1['store_id']:
                item['sales_growth'] = item1['month_on_month']

    # print current_store_list
    for item in current_store_list:
        try:
            int(item["parent_id"]) 
            item['parent_id']=get_city2_by_id(item['parent_id'])
        except Exception as e:
            print item
            item["parent_id"] = ''
            item["target"] = 0
            item["area"] = ''
    # for item in current_store_list:
    #     item['parent_id'] = u'西安'
    all_items_count = len(current_store_list)
    all_page_count = divmod(all_items_count, 20)[0] if divmod(all_items_count,20)[1] == 0 else divmod(all_items_count, 20)[0] + 1

    page_list = [i for i in xrange(1, all_page_count + 1)]
    page_list = map(num_to_chinese, page_list)
    #初始化分页对象
    current_page = request.GET.get('current_page', '1')
    obj = Pagination(current_page, all_items_count)
    # for item in current_store_list:
    #     id=item['parent_id']
    #     if id:
    #         item['parent_id']=get_city2_by_id(id)
    
    current_store_list = current_store_list[obj.start:obj.end]
    all_response_date['all_page_count'] = all_page_count
    all_response_date['page_list'] = page_list
    all_response_date['current_store_list'] = current_store_list

    return HttpResponse(json.dumps(all_response_date))

def get_store_count(start_date,end_date,chainstore_id):
    store_query = pandas.read_sql_query(
        '''
        SELECT
            count(*) as num
        FROM
            store_store ssi 
        INNER JOIN
            summary_dailystoreitemsummary summary
        ON
            (ssi.store_id = summary.store_id)
        INNER JOIN
            store_storedailytarget target
        ON
            (ssi.id = target.store_id)
        INNER JOIN
            store_city city
        ON
            (city.id = ssi.city_id)
        WHERE
            ssi.chainstore_id = %(chainstore_id)s AND
            summary.date >= %(start_date)s AND summary.date <= %(end_date)s    AND
            target.date >= %(start_date)s AND target.date <= %(end_date)s
        GROUP BY ssi.store_id, ssi.name, city.name, city.parent_id
    ''',
    params = {'start_date': start_date, 'end_date': end_date,'chainstore_id':chainstore_id},
    con = connection)
    return store_query['num'][0]

def get_storelist_by_sql(start_date,end_date,chainstore_id):
    data = pandas.read_sql_query(
        sql = '''
            SELECT
                ssi.store_id,
                sum(summary.sales) as sales,
                sum(summary.num) as nums,
                sum(target.sales) as target,
                ssi.name,
                city.name as area,
                city.parent_id
            FROM
                store_store ssi 
            LEFT JOIN
                summary_dailystoreitemsummary summary
            ON
                (ssi.store_id = summary.store_id)
            LEFT JOIN
                store_storedailytarget target
            ON
                (ssi.id = target.store_id)
            LEFT JOIN
                store_city city
            ON
                (city.id = ssi.city_id)
            WHERE
                ssi.chainstore_id = %(chainstore_id)s AND
                summary.date >= %(start_date)s AND summary.date <= %(end_date)s   AND
                target.date >= %(start_date)s AND target.date <= %(end_date)s 
            GROUP BY ssi.store_id, ssi.name, city.name, city.parent_id
        ''',
        params = {'start_date': start_date, 'end_date': end_date,'chainstore_id':chainstore_id},
        con = connection)
    return [row.to_dict() for _, row in data.iterrows()]

def search_storelist_by_sql(start_date,end_date,keywords):
    data = pandas.read_sql_query(
        sql = '''
            SELECT
                ssi.store_id,
                sum(summary.sales) as sales,
                sum(summary.num) as nums,
                sum(target.sales) as target,
                ssi.name,
                city.name as area,
                city.parent_id
            FROM
                store_store ssi 
            INNER JOIN
                summary_dailystoreitemsummary summary
            ON
                (ssi.store_id = summary.store_id)
            INNER JOIN
                store_storedailytarget target
            ON
                (ssi.id = target.store_id)
            INNER JOIN
                store_city city
            ON
                (city.id = ssi.city_id)
            WHERE
                summary.date >= %(start_date)s AND summary.date <= %(end_date)s AND ssi.name like %(keywords)s OR city.name like %(keywords)s
            GROUP BY ssi.store_id, ssi.name, city.name, city.parent_id
        ''',
        params = {'start_date': start_date, 'end_date': end_date,'keywords':'%%%s%%' % keywords},
        con = connection)
    return [row.to_dict() for _, row in data.iterrows()]

@login_required(login_url='/login/')
def special_items(request,store_id):
    # print Store.objects.all().values('id','name')
    #获取排序规则
    sort_rule = request.GET.get('sort_rule','1,1')
    rule,days = sort_rule.split(',')
    rule_dict = {
        1:{'rule':'sales','rule1':'DESC'},
        2:{'rule':'sales','rule1':'ASC'},
        3:{'rule':'num','rule1':'DESC'},
        4:{'rule':'num','rule1':'ASC'},
    }
    days_dict = {
        1:7,
        2:30,
        3:90
    }
    result = rule_get_store_top_items(store_id, days = days_dict[int(days)], rule1 = rule_dict[int(rule)]['rule'], rule2 = rule_dict[int(rule)]['rule1'])[:20]
    day1, day2, day3, day4 = range_date(days_dict[int(days)])
    sales_growth = get_storeitem_sales_increase(day1, day2, day3, day4, store_id)
    num_growth = get_storeitem_num_increase(day1, day2, day3, day4, store_id)
    for item in result:
        for item1 in sales_growth:
            if item['item_id'] == item1['item_id']:
                item['sales_growth'] = item1['month_on_month_sales']
        for item2 in num_growth:
            if item['item_id'] == item2['item_id']:
                item['num_growth'] = item2['month_on_month_num']

                                                                                                                                                                                                                           
    return HttpResponse(json.dumps(result))

@login_required(login_url='/login/')
def get_overall_data(request):
    user = request.user
    chainstore_id=StoreUser.objects.filter(user__username=user).values('permission__chain_store_permission').first()['permission__chain_store_permission']
    all_response_date = {}
    date_rule=request.GET.get('date_rule', '1')
    if date_rule in ['1','2','3']:
        if date_rule =='1':#yesterday
            start_date = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
            end_date = datetime.date.today().strftime('%Y-%m-%d')
            day_or_month_list = start_date.split('-')[2]
        elif date_rule == '2':#current_week
            start_date, end_date, day_or_month_list,total_day_list = current_week()
        elif date_rule == '3':#current_month
            start_date, end_date, day_or_month_list = current_month()
        chart_date = get_each_day_sales_by_week_or_by_month(start_date, end_date, chainstore_id)
        flag = False
        for item in chart_date:
            if item['d'] == datetime.date.today().strftime('%Y-%m-%d'):
                flag = True
        if not flag:
            chart_date.append({"num_trades": 0, "each_num_trades_sales": 0, "d": datetime.date.today().strftime('%Y-%m-%d'), "sales":0})

    else:
        if date_rule == '4':#current_quarter
            start_date, end_date, day_or_month_list = current_quarter()
        else:#current_year
            start_date, end_date, day_or_month_list = current_year()
        chart_date = get_each_month_sales_by_year_or_by_quarter(start_date, end_date, chainstore_id)
    overall_data = get_total_sales_by_days(start_date, end_date, chainstore_id)
    day_or_month_list = day_or_month_list if day_or_month_list else 0

    for item in overall_data:
        for k, v in item.items():
            if not v :
                item[k] = 0
    #区域部分
    area_list = get_area_list_sales(start_date,end_date,chainstore_id)
    for item in area_list:
        try:
            int(item["finish_rate"]) 
        except Exception as e:
            item["finish_rate"] = 0
            item["tsales"] = 0
            item["balance"] = 0
    print area_list
    all_response_date['area_list'] = area_list
    all_response_date['overall_data'] = overall_data
    all_response_date['Y_axis'] = chart_date if chart_date else [0]
    len_Y_axis = len(all_response_date['Y_axis'])
    all_response_date['X_axis'] = day_or_month_list[(len(day_or_month_list) - len_Y_axis):]  #根据纵坐标长度对横坐标进行切片

    return HttpResponse(json.dumps(all_response_date))

def store_overview(request, template = 'analytics/store_overview.html'):
    return render(request, template)

def store_analysis(request, template = 'analytics/store_analysis.html'):
    return render(request, template)

def store_detailed_info(request, template = 'analytics/store_detailed_info.html'):
    return render(request, template)

@login_required(login_url='/login/')
def get_store_overall_data(request,store_id):
    chain_store_uac, stores_uac, categories_uac, areas = get_user_uac(request.user)
    if not chain_store_uac:
        return HttpResponse(json.dumps(response), content_type='application/json')
    term_range = request.GET.get('date_rule', WEEKLY)

    store_property = request.GET.get('store_property', 1)
    all_response_date={}
    date_rule=request.GET.get('date_rule1','1')
    print date_rule
    if date_rule=='1':#yesterday
        start_date = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        end_date = datetime.date.today().strftime('%Y-%m-%d')
        day_or_month_list=start_date.split('-')[2]
        print start_date,end_date,day_or_month_list
    elif date_rule=='2':#current_week
        start_date,end_date,day_or_month_list,total_day_list=current_week()
        print start_date,end_date,day_or_month_list
    elif date_rule=='3':#current_month
        start_date,end_date,day_or_month_list=current_month()
        print start_date,end_date,day_or_month_list
    if date_rule == '4':#current_quarter
        start_date, end_date, day_or_month_list = current_quarter()
    else:#current_year
        start_date, end_date, day_or_month_list = current_year()
    all_response_date['X_axis'],all_response_date['Y_axis'] = overall_store_chart(term_range,store_property,chain_store_uac,int(store_id))
    overall_data = get_store_overall_date_by_redis(start_date,end_date,store_id,chain_store_uac)
    

    all_response_date['overall_data'] = overall_data

    return HttpResponse(json.dumps(all_response_date))

def get_store_each_day_sales_by_week_or_by_month(start_date,end_date,store_id):
    data = pandas.read_sql_query(
        sql = '''
            SELECT
                to_char(summary.date, 'YYYY-MM-DD') as d,
                sum(summary.sales) as sales,
                sum(summary.num) as num_trades,
                round(cast ( sum(summary.sales) / sum(summary.num) as numeric ), 2) as each_num_trades_sales
            FROM
                summary_dailystoreitemsummary summary
            LEFT JOIN 
                store_store  store
            ON 
                summary.store_id=store.store_id
            WHERE
                store.store_id = %(store_id)s AND
                summary.date >= %(start_date)s AND summary.date <= %(end_date)s
            GROUP BY d
        ''',
        params = {'start_date': start_date, 'end_date': end_date, 'store_id':store_id},
        con = connection)
    return [row.to_dict() for _, row in data.iterrows()]

def get_store_total_sales_by_days(start_date,end_date,store_id):
    data = pandas.read_sql_query(
        sql = '''
            SELECT
                sum(summary.sales) as sales,
                sum(summary.num) as num_trades,
                round(cast ( sum(summary.sales) / sum(summary.num) as numeric ), 2)as each_num_trades_sales
            FROM
                summary_dailystoreitemsummary summary
            LEFT JOIN 
                store_store  store
            ON 
                summary.store_id=store.store_id
            WHERE
                store.store_id = %(store_id)s AND
                summary.date >= %(start_date)s AND summary.date <= %(end_date)s
        ''',
        params = {'start_date': start_date, 'end_date': end_date, 'store_id':store_id},
        con = connection)
    return [row.to_dict() for _, row in data.iterrows()]   

def get_store_each_month_sales_by_year_or_by_quarter(start_date,end_date,store_id):
    year, month, day=datetime.date.today().strftime('%Y-%m-%d').split('-')
    month=int(month)
    start_date_list = [year + '-01-01', year + '-02-01', year + '-03-01',year + '-04-01', year + '-05-01', year + '-06-01', year + '-07-01', year + '-08-01', year + '-09-01', year + '-10-01', year + '-11-01', year + '-12-01']
    
    data = pandas.read_sql_query(
        sql = '''
            SELECT
                to_char(summary.date, 'YYYY-MM') as d,
                sum(summary.sales) as sales,
                sum(summary.num) as num_trades,
                round(cast ( sum(summary.sales) / sum(summary.num) as numeric ), 2) as each_num_trades_sales
            FROM
                summary_dailystoreitemsummary summary
            LEFT JOIN 
                store_store  store
            ON 
                summary.store_id = store.store_id
            WHERE
                store.store_id = %(store_id)s AND
                summary.date >= %(start_date)s AND summary.date <= %(end_date)s
            GROUP BY d
        ''',
        params = {'start_date': start_date, 'end_date': end_date,'store_id':store_id},
        con = connection)
    return [row.to_dict() for _, row in data.iterrows()]

def get_area_list_sales(start_date,end_date,chainstore_id):
    print start_date,end_date
    data = pandas.read_sql_query(
        sql = '''
            SELECT
                attribute.name as name,
                round(cast (sum(target.sales)as numeric ), 2) as tsales,
                round(cast (sum(summary.sales) as numeric ), 2) as sales,
                round(cast (sum(summary.sales) / sum(target.sales) as numeric ), 2) as finish_rate,
                round(cast (sum(target.sales) - sum(summary.sales) as numeric ), 2) as balance
            FROM
                store_attributemap attributemap
            LEFT JOIN
                store_store ssi
            ON
                (ssi.id =attributemap.store_id)
            LEFT JOIN
                store_attribute attribute
            ON
                (attribute.id = attributemap.attribute_id)
            LEFT JOIN
                summary_dailystoreitemsummary summary
            ON
                (ssi.store_id = summary.store_id)
            LEFT JOIN
                store_storedailytarget target
            ON
                (ssi.id = target.store_id)
            WHERE
                ssi.chainstore_id = %(chainstore_id)s AND
                attribute.attr_type = 'AREA' AND
                summary.date >= %(start_date)s AND summary.date <= %(end_date)s  AND
                target.date >= %(start_date)s AND target.date <= %(end_date)s 
            GROUP BY attribute.name
            
        ''',
        params = {'start_date': start_date, 'end_date': end_date, 'chainstore_id': chainstore_id},
        con = connection)
    return [row.to_dict() for _, row in data.iterrows()]

def get_store_hot_item(request,store_id):
    print store_id
    #获取排序规则
    days = request.GET.get('days','1')
    days_dict = {
        1:7,
        2:30,
        3:90
    }
    # print days_dict[int(days)]
    result = rule_get_store_top_items_by_category(store_id,days = days_dict[int(days)])
    i = 0
    while i<len(result):
        try:
            if int(result[i]["parent_id"]) :
                i += 1
        except Exception as e:
            del result[i] 
    for item in result:
        level0_name = get_level0_name(int(item['parent_id']))
        del item["parent_id"]
        del item["name"]
        del item["store_id"]
        item['level0_name'] = level0_name
    ret = {}
    for item in result:
        if item['level0_name'] not in ret:
            ret[item['level0_name']] = item
        else:
            ret[item['level0_name']]['num'] += item['num']
            ret[item['level0_name']]['sales'] += item['sales']
    ret=ret.values()
    r={}
    for item in ret:
        for k, v in item.items():
            if k not in r:
                r[k] = []
                r[k].append(v)
            else:
                r[k].append(v)

                                                                                                                                                                                                                          
    return HttpResponse(json.dumps(r))

def rule_get_store_top_items_by_category(store_id,days):
    start_date = (datetime.date.today() - datetime.timedelta(days=days)).strftime('%Y-%m-%d')
    end_date = datetime.date.today().strftime('%Y-%m-%d')

    data = pandas.read_sql_query(
        sql = '''
            SELECT
                sum(dailystorecategorysummary.num) as num,
                sum(dailystorecategorysummary.sales) as sales,
                storecategory.name,
                ssi.store_id as store_id,
                storecategory.parent_id as parent_id
            FROM
                summary_dailystorecategorysummary dailystorecategorysummary
            LEFT JOIN 
                store_storecategory  storecategory
            ON 
                storecategory.id = dailystorecategorysummary.category_id
            LEFT JOIN
                store_store ssi
            ON
                (dailystorecategorysummary.store_id = ssi.id)
            WHERE 
                ssi.store_id = %(store_id)s AND
                dailystorecategorysummary.date >= %(start_date)s AND dailystorecategorysummary.date <= %(end_date)s 
            GROUP BY dailystorecategorysummary.category_id, ssi.store_id, storecategory.name, storecategory.parent_id
        ''',
        params = {'start_date': start_date, 'end_date': end_date, 'store_id': store_id},
        con = connection)
    return [row.to_dict() for _, row in data.iterrows()]

def get_level0_name(id1):
    store_query = pandas.read_sql_query(
        '''
        SELECT
            name
        FROM
            store_storecategory storecategory 
        WHERE storecategory.id = %(id1)s 
    ''',
    params = {'id1': id1},
    con = connection)
    return store_query['name'][0]

def month_date():
        d = datetime.datetime.now()
        year = d.year
        month = d.month
        if month == 1 :
            month = 12
            year -= 1
        else :
            month -= 1
        last_month_1st = datetime.datetime(year,month,1).strftime('%Y-%m-%d')
        last_month_today = datetime.datetime(year, month, d.day).strftime('%Y-%m-%d')
        this_month_1st = datetime.datetime(year,d.month,1).strftime('%Y-%m-%d')
        today = datetime.datetime(year,d.month,d.day).strftime('%Y-%m-%d')
        return last_month_1st, last_month_today, this_month_1st, today

def year_date():
        d = datetime.datetime.now()
        year = d.year
        month = d.month
        last_year_1st = datetime.datetime(year-1,1,1).strftime('%Y-%m-%d')
        last_year_today = datetime.datetime(year-1, month, d.day).strftime('%Y-%m-%d')
        this_year_1st = datetime.datetime(year,1,1).strftime('%Y-%m-%d')
        today = datetime.datetime(year,d.month,d.day).strftime('%Y-%m-%d')
        return last_year_1st, last_year_today, this_year_1st, today

def week_date():
    current_week_day = datetime.datetime.now().weekday()
    last_week_1st = (datetime.date.today() - datetime.timedelta(days=(current_week_day+7))).strftime('%Y-%m-%d')
    last_week_today = (datetime.date.today() - datetime.timedelta(days=(7))).strftime('%Y-%m-%d')
    this_week_1st = (datetime.date.today() - datetime.timedelta(days=(current_week_day))).strftime('%Y-%m-%d')
    today = datetime.date.today().strftime('%Y-%m-%d')
    return  last_week_1st, last_week_today, this_week_1st,today
def range_date(day):
    last_week_1st = (datetime.date.today() - datetime.timedelta(days = day * 2)).strftime('%Y-%m-%d')
    last_week_today = (datetime.date.today() - datetime.timedelta(days = day)).strftime('%Y-%m-%d')
    this_week_1st = (datetime.date.today() - datetime.timedelta(days = day)).strftime('%Y-%m-%d')
    today = datetime.date.today().strftime('%Y-%m-%d')
    return  last_week_1st, last_week_today, this_week_1st, today 

def get_store_sales_increase(day1, day2, day3, day4, chainstore_id):
    data = pandas.read_sql_query(
        sql = '''
            SELECT (sd1.sums-sd2.sums) AS month_on_month,
               ss.id,
               ss.store_id
            FROM store_store ss
            RIGHT JOIN
                (SELECT store_id,
                  sum(sales) AS sums
                FROM summary_dailystoresummary''' + ' ' +
                "WHERE date>'" + day1 + "'  " +
                    "AND date<'" + day2 + "'  " +
                '''GROUP BY store_id) AS sd1 ON sd1.store_id=ss.id
                RIGHT JOIN
              (SELECT store_id,
                      sum(sales) AS sums
               FROM summary_dailystoresummary''' + ' '
               "WHERE date>'" + day3 + "'  " +
                " AND date<'" + day4 + "' " +
               '''GROUP BY store_id) AS sd2 ON sd2.store_id=ss.id
               WHERE ss.chainstore_id=%(chainstore_id)s
        ''',
        params = {'chainstore_id':chainstore_id},
        con = connection)
    return [row.to_dict() for _, row in data.iterrows()]   
    

def get_storeitem_turnover(day1,day2,store_id):
    data = pandas.read_sql_query(
        sql = '''
            SELECT
                round(cast (2 * summary.num / (sd1.quantity + sd2.quantity) as numeric ), 2) as num
            FROM
                store_store ss
            RIGHT JOIN
                summary_dailystoreitemsummary summary
            ON 
                (ss.store_id = summary.store_id)
            RIGHT JOIN
                (SELECT  quantity,store_id 
                    FROM store_storeiteminventory''' + ' ' +
                    "WHERE store_storeiteminventory.fill_date='" + day1 + "'  " +
                    "AND store_id='" + str(store_id) + "'  " + ') AS sd1 ON sd1.store_id=ss.id' + ' ' +
                    '''RIGHT JOIN
                    (SELECT quantity,store_id 
                    FROM store_storeiteminventory''' + ' ' +
                    "WHERE store_storeiteminventory.fill_date='" + day2 + "'  " +
                    "AND store_id='" + str(store_id) + "'  " + ') AS sd2 ON sd2.store_id=ss.id' + ' ' +
        '''
            WHERE''' + ' ' +
                "ss.store_id='" + str(store_id) + "'  " + 'AND' + ' ' +
                "summary.date >='" + day1 + "'  " +
                " AND summary.date <='" +
                day2 + "'"
        ,
        params = {'store_id':store_id},
        con = connection)
    return [row.to_dict() for _, row in data.iterrows()]   

def get_storeitem_sales_increase(day1,day2,day3,day4,store_id):
    data = pandas.read_sql_query(
        sql = '''
            SELECT (sd1.sums-sd2.sums) AS month_on_month_sales,
                sd1.item_id
            FROM 
                (SELECT item_id,store_id,
                  sum(sales) AS sums
                FROM summary_dailystoreitemsummary''' + ' '
                "WHERE date >'" + day1 + "'  " +
                    "AND date <'" + day2 + "'  " +
                '''GROUP BY item_id,store_id) AS sd1 
                RIGHT JOIN
              (SELECT item_id,store_id,
                      sum(sales) AS sums
               FROM summary_dailystoreitemsummary''' + ' '
               "WHERE date >'" + day3 + "'  " +
                " AND date <'" + day4 + "' " +
               '''GROUP BY item_id,store_id) AS sd2 ON sd2.item_id=sd1.item_id
               WHERE sd1.store_id = %(store_id)s
        ''',
        params = {'store_id': store_id},
        con = connection)
    return [row.to_dict() for _, row in data.iterrows()]

def get_storeitem_num_increase(day1, day2, day3, day4, store_id):
    data = pandas.read_sql_query(
        sql = '''
            SELECT (sd1.sums-sd2.sums) AS month_on_month_num,
                sd1.item_id
            FROM 
                (SELECT item_id,store_id,
                  sum(num) AS sums
                FROM summary_dailystoreitemsummary''' + ' '
                "WHERE date >'"+ day1 + "'  " +
                    "AND date <'" + day2 + "'  " +
                '''GROUP BY item_id,store_id) AS sd1 
                RIGHT JOIN
              (SELECT item_id,store_id,
                      sum(num) AS sums
               FROM summary_dailystoreitemsummary''' + ' '
               "WHERE date>'" + day3 + "'  " +
                " AND date<'" + day4 + "' " +
               '''GROUP BY item_id, store_id) AS sd2 ON sd2.item_id=sd1.item_id
               WHERE sd1.store_id = %(store_id)s
        ''',
        params = {'store_id':store_id},
        con = connection)
    return [row.to_dict() for _, row in data.iterrows()]    


def test(request):
    # StoreUser.objects.create(user_id=35,permission_id=1)
    # UAC.objects.create(login_to_url='/login/')

    # obj=ChainStore.objects.get(id=32)
    # obj1=UAC.objects.get(id=1)
    # obj1.chain_store_permission.add(obj)
    # obj1=UAC.objects.all().values('chain_store_permission','login_to_url','id')
    # StoreUser.objects.create(user_id=35,permission_id=1)
    # obj1=StoreUser.objects.all().values('user','permission_id')

    # print obj1
    # user = request.user
    # chainstore_id=StoreUser.objects.filter(user__username=user).values('permission__chain_store_permission').first()['permission__chain_store_permission']
    # # print 
    # print redisC.smembers('sales:2016-11-01')
    chainstore_id=32
    store_id=1000185
    start_date = (datetime.date.today() - datetime.timedelta(days=(7))).strftime('%Y-%m-%d')
    end_date = datetime.date.today().strftime('%Y-%m-%d')
    tsales=get_store_quantity(start_date,end_date,store_id,chainstore_id)
    # tsales=get_category(32)
    return HttpResponse(json.dumps(tsales))

def get_store_tsales_by_redis(start_date,end_date,store_id,chainstore_id):

    start_date,end_date=get_date(start_date,end_date)
    result={}
    
    while start_date<=end_date:
        r=redisC.smembers('daily_target:%s:chainstore_id:%s' % (str(start_date), chainstore_id))
        for item in r:
            l=json.loads(item)
            if l['store_id']==store_id:
                if store_id not in result:
                    result[store_id]=[]
                    result[store_id].append(l)
                else:
                    result[store_id].append(l)
        start_date = start_date + datetime.timedelta(days=1)
    s=0
    for item in result[store_id]:
        s+=item['sales']
    return s


def get_date(start_date,end_date):
    year1,month1,day1=start_date.split('-')
    year2,month2,day2=end_date.split('-')
    start_date=datetime.date(int(year1),int(month1),int(day1))
    end_date=datetime.date(int(year2),int(month2),int(day2))
    return start_date,end_date

def get_store_name_and_city(store_id):
    obj=Store.objects.get(store_id=store_id)
    name=obj.name
    city_id=obj.city_id
    obj1=City.objects.get(id=city_id)
    area=obj1.name
    cityid=obj1.parent_id
    cityname=City.objects.get(id=cityid).name
    return name+'('+cityname+area+')'

def get_store_sales_by_redis(start_date,end_date,store_id,chainstore_id):

    start_date,end_date=get_date(start_date,end_date)
    result={}
    
    while start_date<=end_date:
        r=redisC.smembers('sales:%s:chainstore_id:%s' % (str(start_date), chainstore_id))
        for item in r:
            l=json.loads(item)
            if l['store_id']==store_id:
                if store_id not in result:
                    result[store_id]=[]
                    result[store_id].append(l)
                else:
                    result[store_id].append(l)
        start_date = start_date + datetime.timedelta(days=1)
    s=0
    for item in result[store_id]:
        s+=item['sales']
    return s

def get_store_balance(start_date,end_date,store_id,chainstore_id):
    tsales=get_store_tsales_by_redis(start_date,end_date,store_id,chainstore_id)
    sales=get_store_sales_by_redis(start_date,end_date,store_id,chainstore_id)
    balance=sales-tsales
    return balance

def get_store_num(start_date,end_date,store_id,chainstore_id):

    start_date,end_date=get_date(start_date,end_date)
    result={}
    
    while start_date<=end_date:
        r=redisC.smembers('sales:%s:chainstore_id:%s' % (str(start_date), chainstore_id))
        for item in r:
            l=json.loads(item)
            if l['store_id']==store_id:
                if store_id not in result:
                    result[store_id]=[]
                    result[store_id].append(l)
                else:
                    result[store_id].append(l)
        start_date = start_date + datetime.timedelta(days=1)
    s=0
    for item in result[store_id]:
        s+=item['num']
    return s 

def get_store_quantity(start_date,end_date,store_id,chainstore_id):
    r=get_store_quantity_by_cateory(start_date,end_date,store_id,chainstore_id)
    s=0
    if r:
        s=sum(r.values)
    return s 

def get_store_turnover(start_date,end_date,store_id,chainstore_id):
    num=get_store_num(start_date,end_date,store_id,chainstore_id)
    quantity=get_store_quantity(start_date,end_date,store_id,chainstore_id)
    turnover=num/quantity

    return turnover

def get_store_gross_profit(start_date,end_date,store_id,chainstore_id):
    start_date,end_date=get_date(start_date,end_date)
    result={}
    
    while start_date<=end_date:
        print start_date
        r=redisC.smembers('gross_profit:%s:chainstore_id:%s' % (str(start_date), chainstore_id))
        for item in r:
            l=json.loads(item)
            if int(l['store_id'])==store_id:
                print store_id
                if store_id not in result:
                    result[store_id]=[]
                    result[store_id].append(l)
                else:
                    result[store_id].append(l)
        start_date = start_date + datetime.timedelta(days=1)
    try:
        s=0
        for item in result[store_id]:
            s+=item['gross_profit']
        return s 
    except Exception as e:
        return result

def get_store_overall_date_by_redis(start_date,end_date,store_id,chainstore_id):
    store_name=get_store_name_and_city(store_id)
    sales=get_store_sales_by_redis(start_date,end_date,store_id,chainstore_id)
    tsales=get_store_tsales_by_redis(start_date,end_date,store_id,chainstore_id)
    balance=get_store_balance(start_date,end_date,store_id,chainstore_id)
    total_turnover=get_store_turnover(start_date,end_date,store_id,chainstore_id)
    gross_profit=get_store_gross_profit(start_date,end_date,store_id,chainstore_id)

    r={}
    r['store_name']=store_name
    r['sales']=sales
    r['tsales']=tsales
    r['balance']=balance
    r['total_turnover']=total_turnover
    r['gross_profit']=gross_profit

    return r


def get_category(chainstore_id):
    level0=redisC.smembers('category:chainstore:%s:level:0' % ( chainstore_id))
    l0=[]
    for item in level0:
        l0.append(json.loads(item))

    level1=redisC.smembers('category:chainstore:%s:level:1' % ( chainstore_id))
    l1=[]
    for item in level1:
        l1.append(json.loads(item))


    level2=redisC.smembers('category:chainstore:%s:level:2' % ( chainstore_id))
    l2=[]
    for item in level2:
        l2.append(json.loads(item))
    return [l0,l1,l2]

def get_store_data_by_category(start_date,end_date,store_id,chainstore_id):
    start_date,end_date=get_date(start_date,end_date)
    result={}
    id=Store.objects.get(store_id=store_id).id

    while start_date<=end_date:
        print start_date
        r=redisC.smembers('store_item:%s:chainstore:%s:store:%s' % (str(start_date), chainstore_id,id))
        print len(r)
        for item in r:
            l=json.loads(item)
            if int(l['store_id'])==store_id:
                # print store_id

                try:
                    int(l['store_cat_id'])
                except Exception as e:
                    l['store_cat_id']=0
                if l['store_cat_id'] not in result:
                    result[int(l['store_cat_id'])]=[]
                    result[int(l['store_cat_id'])].append(l)
                else:
                    result[int(l['store_cat_id'])].append(l)
        start_date = start_date + datetime.timedelta(days=1)
    return result 

def leval2_self_to_merger(start_date,end_date,store_id,chainstore_id):
    result=get_store_data_by_category(start_date,end_date,store_id,chainstore_id)
    #leval2_self_to_merger
    s={}
    for k,j in result.items():
        for v in j:
            try:
                int(v['num'])
            except:
                v['num']=0
            try:
                int(v['sales'])
            except:
                v['sales']=0
            try:
                int(v['gross_profit'])
            except:
                v['gross_profit']=0
            if k not in s:
                s[k]={}
                if 'num' not in s[k]:
                    s[k]['num']=0

                    s[k]['num']+=v['num'] 
                else:
                    s[k]['num']+=v['num']

                if 'sales' not in s[k]:
                    s[k]['sales']=0
                    s[k]['sales']+=v['sales']
                else:
                    s[k]['sales']+=v['sales']

                if 'gross_profit' not in s[k]:
                    s[k]['gross_profit']=0
                    s[k]['gross_profit']+=v['gross_profit']
                else:
                    s[k]['gross_profit']+=v['gross_profit']
            else:
                if 'num' not in s[k]:
                    s[k]['num']=0
                    s[k]['num']+=v['num']
                else:
                    s[k]['num']+=v['num']

                if 'sales' not in s[k]:
                    s[k]['sales']=0
                    s[k]['sales']+=v['sales']
                else:
                    s[k]['sales']+=v['sales']

                if 'gross_profit' not in s[k]:
                    s[k]['gross_profit']=0
                    s[k]['gross_profit']+=v['gross_profit']
                else:
                    s[k]['gross_profit']+=v['gross_profit']
    return s

def leval2_to_leval0_data(start_date,end_date,store_id,chainstore_id):
    category_data=leval2_self_to_merger(start_date,end_date,store_id,chainstore_id)
    s={}
    level0_set = redisC.smembers('category:chainstore:%s:level:0' % (chainstore_id))
    level1_set = redisC.smembers('category:chainstore:%s:level:1' % (chainstore_id))
    level2_set = redisC.smembers('category:chainstore:%s:level:2' % (chainstore_id))
    category_set = level0_set | level1_set | level2_set
    categories = [json.loads(category) for category in category_set]
    for k,v in category_data.items():
        k1=get_level0_category_name(int(k),categories)
        if k1 not in s:
            s[k1]={}
            if 'num' not in s[k1]:
                s[k1]['num']=0

                s[k1]['num']+=v['num'] 
            else:
                s[k1]['num']+=v['num']

            if 'sales' not in s[k1]:
                s[k1]['sales']=0
                s[k1]['sales']+=v['sales']
            else:
                s[k1]['sales']+=v['sales']

            if 'gross_profit' not in s[k1]:
                s[k1]['gross_profit']=0
                s[k1]['gross_profit']+=v['gross_profit']
            else:
                s[k1]['gross_profit']+=v['gross_profit'] 
        else:
            if 'num' not in s[k1]:
                s[k1]['num']=0

                s[k1]['num']+=v['num'] 
            else:
                s[k1]['num']+=v['num']

            if 'sales' not in s[k1]:
                s[k1]['sales']=0
                s[k1]['sales']+=v['sales']
            else:
                s[k1]['sales']+=v['sales']

            if 'gross_profit' not in s[k1]:
                s[k1]['gross_profit']=0
                s[k1]['gross_profit']+=v['gross_profit']
            else:
                s[k1]['gross_profit']+=v['gross_profit'] 
    return s

def get_store_quantity_by_cateory(start_date,end_date,store_id,chainstore_id):
    print start_date,end_date
    start_date,end_date=get_date(start_date,end_date)
    id=Store.objects.get(store_id=store_id).id
    start_quantity=0
    end_quantity=0
    
        
    items_set_start = redisC.smembers('store_item:%s:chainstore:%s:store:%d' % (start_date, chainstore_id,store_id))
    items_set_end = redisC.smembers('store_item:%s:chainstore:%s:store:%d' % (end_date, chainstore_id,store_id))
    level0_set = redisC.smembers('category:chainstore:%s:level:0' % (chainstore_id))
    level1_set = redisC.smembers('category:chainstore:%s:level:1' % (chainstore_id))
    level2_set = redisC.smembers('category:chainstore:%s:level:2' % (chainstore_id))
    category_set = level0_set | level1_set | level2_set
    categories = [json.loads(category) for category in category_set]
    print len(items_set_start),len(items_set_end),111
    term_start_result = {}
    term_end_result = {}
    for _row in items_set_start:
        row = json.loads(_row)
        category_id = row.get('store_cat_id')
        if category_id:
            cat_id = get_level0_category_id(int(category_id), categories)
            if not term_start_result.get(cat_id):
                term_start_result[cat_id] = 0
            term_start_result[cat_id] += row.get('quantity')
    for _row in items_set_end:
        row = json.loads(_row)
        category_id = row.get('store_cat_id')
        if category_id:
            cat_id = get_level0_category_id(int(category_id), categories)
            if not term_end_result.get(cat_id):
                term_end_result[cat_id] = 0
            term_end_result[cat_id] += row.get('quantity')
    result={}
    for k,v in term_start_result.items():
        for k1,v1 in term_end_result.items():
           term_start_result[k]+=v1
           term_start_result[k]=term_start_result[k]/2       
    return term_start_result 

def get_level0_category_name(category_id, categories):
    level = -1
    while level != 0:
        for category in categories:
            if category.get('category_id') == category_id:
                if int(category.get('level')) != 0:
                    category_id = category.get('parent_id')
                    level = category.get('level')
                else:
                    level = 0
                break
    return category.get('name')

def get_store_turnover_by_cateory(start_date,end_date,store_id,chainstore_id):
    r=leval2_to_leval0_data(start_date,end_date,store_id,chainstore_id)
    s=get_store_quantity_by_cateory(start_date,end_date,store_id,chainstore_id)
    for k,v in r.items():
        for k1,v1 in s.items():
            if k==k1:
                r['turnover']=v['num']/v1
    return r

def get_term_start_date(date, term_range):
    if isinstance(date, str):
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    if term_range == TODAY:
        date = date
    elif term_range == YESTERDAY:
        date = date - datetime.timedelta(days=1)
    elif term_range == WEEKLY:
        while date.weekday() != 0:
            date = date - datetime.timedelta(days=1)
    elif term_range == MONTHLY:
        while date.day != 1:
            date = date - datetime.timedelta(days=1)
    elif term_range == SEASONALLY:
        while date.month not in (1, 4, 7, 10) or date.day != 1:
            date = date - datetime.timedelta(days=1)
    elif term_range == YEARLY:
        while date.month != 1 or date.day != 1:
            date = date - datetime.timedelta(days=1)
    return date


def get_term_on_term_date(date, term_range):
    if isinstance(date, str):
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    if term_range == WEEKLY:
        date = date - datetime.timedelta(weeks=1)
    elif term_range == MONTHLY:
        date = datetime.date(date.year, date.month - 1, date.day)
    elif term_range == SEASONALLY:
        date = datetime.date(date.year, date.month - 3, date.day)
    elif term_range == YEARLY:
        date = datetime.date(date.year - 1, date.month, date.day)
    return date, get_term_start_date(date, term_range)

def get_user_uac(user):
    store_user = StoreUser.objects.filter(user=user)
    if store_user.count() == 0:
        return None
    store_user = store_user[0]
    area_stores = set()
    categories = set()
    areas = {}
    chain_store_permission = store_user.permission.chain_store_permission
    for item in store_user.permission.store_area_permission.all():
        _stores = redisC.smembers('Attr:%s:%s' % (item.attr_type, item.id))
        _area = {'stores': [], 'name': ''}
        for _store in _stores:
            store = json.loads(_store)
            _area['stores'].append(store.get('id'))
            _area['name'] = store.get('name')
        areas[item.id] = _area
        [area_stores.add(int(json.loads(_store).get('id'))) for _store in _stores]
    [categories.add(category.id) for category in store_user.permission.store_area_permission.all()]
    return chain_store_permission.id, area_stores, categories, areas

def overall_data(request):
    response = {'success': 0, 'data': {}}
    chain_store_uac, stores_uac, categories_uac, areas = get_user_uac(request.user)
    if not chain_store_uac:
        return HttpResponse(json.dumps(response), content_type='application/json')
    term_range = request.GET.get('date_rule', WEEKLY)

    store_property = request.GET.get('store_property', 1)
    property_stores_set = set()
    [property_stores_set.add(json.loads(store).get('id')) for store in redisC.smembers('Attr:PROPERTY:%d' % store_property)]
    stores_uac = stores_uac & property_stores_set
    date = get_term_start_date(datetime.date.today(), term_range)
    sales = 0.0
    sales_target = 0.0
    gross_profit = 0.0
    num_trades = 0.0
    num = 0.0
    term_beginning_invnetory = 0.0
    term_end_inventory = 0.0
    term_beginning_invnetory_set = redisC.smembers('inventory:%s:chainstore_id:%d' % (date, chain_store_uac))
    for _row in term_beginning_invnetory_set:
        row = json.loads(_row)
        if int(row.get('id')) in stores_uac:
            term_beginning_invnetory += 0 if not row.get('quantity_sum') else row.get('quantity_sum')
    term_end_invnetory_set = redisC.smembers('inventory:%s:chainstore_id:%d' % (datetime.date.today() - datetime.timedelta(days=1), chain_store_uac))
    for _row in term_end_invnetory_set:
        row = json.loads(_row)
        if int(row.get('id')) in stores_uac:
            term_end_inventory += 0 if not row.get('quantity_sum') else row.get('quantity_sum')
    while date <= datetime.date.today():
        sales_target_set = redisC.smembers('daily_target:%s:chainstore_id:%s' % (date, chain_store_uac))
        for _row in sales_target_set:
            row = json.loads(_row)
            if int(row.get('id')) in stores_uac:
                sales_target += 0 if not row.get('sales') else row.get('sales')
                for _, _area in areas.items():
                    if int(row.get('id')) in _area.get('stores'):
                        if _area.get('sales_target'):
                            areas[_]['sales_target'] += 0 if not row.get('sales') else row.get('sales')
                        else:
                            areas[_]['sales_target'] = 0 if not row.get('sales') else row.get('sales')
        sales_set = redisC.smembers('sales:%s:chainstore_id:%s' % (date, chain_store_uac))
        for _row in sales_set:
            row = json.loads(_row)
            if int(row.get('id')) in stores_uac:
                sales += 0 if not row.get('sales') else row.get('sales')
                num_trades += 0 if not row.get('num_trades') else row.get('num_trades')
                num += 0 if not row.get('num') else row.get('num')
                for _, _area in areas.items():
                    if int(row.get('id')) in _area.get('stores'):
                        if _area.get('sales'):
                            areas[_]['sales'] += 0 if not row.get('sales') else row.get('sales')
                        else:
                            areas[_]['sales'] = 0 if not row.get('sales') else row.get('sales')
        gross_profit_set = redisC.smembers('gross_profit:%s:chainstore_id:%s' % (date, chain_store_uac))
        for _row in gross_profit_set:
            row = json.loads(_row)
            if int(row.get('id')) in stores_uac:
                if row.get('gross_profit'):
                    print row.get('gross_profit')
                gross_profit += 0.0 if not row.get('gross_profit') else row.get('gross_profit')
                for _, _area in areas.items():
                    if int(row.get('id')) in _area.get('stores'):
                        if _area.get('gross_profit'):
                            areas[_]['gross_profit'] += 0 if not row.get('gross_profit') else row.get('gross_profit')
                        else:
                            areas[_]['gross_profit'] = 0 if not row.get('gross_profit') else row.get('gross_profit')
        date = date + datetime.timedelta(days=1)
    inventory_turnover_ratio = num / (term_beginning_invnetory+term_end_inventory) / 2
    if num_trades!=0:
            trade_unit_price = sales / num_trades 
    else:
        trade_unit_price=0
    difference = sales - sales_target
    if sales!=0:
            gross_profit_rate = gross_profit / sales
    else:
        gross_profit_rate=0
    if sales_target!=0:
            completion_rate = sales / sales_target
    else:
        completion_rate=0
    all_response_date={}
    overall_data={}
    overall_data['tsales']=sales_target
    overall_data['finsh_rate']=completion_rate
    overall_data['balance']=difference
    overall_data['total_turnover']=inventory_turnover_ratio
    overall_data['sales']=sales
    overall_data['gross_profit']=gross_profit
    overall_data['num_trades']=num_trades
    overall_data['each_num_trades_sales']=trade_unit_price
    all_response_date['overall_data']=overall_data
    s=areas.values()
    for item in s:
        if not item.get('sales',''):
            del item

    all_response_date['area_list']= s
    all_response_date['X_axis'],all_response_date['Y_axis']=overall_chart(term_range,store_property,chain_store_uac,stores_uac)
    return HttpResponse(json.dumps(all_response_date))

def stores_list(request):
    response = {'success': 0, 'data': {}}
    chain_store_uac, stores_uac, categories_uac, areas = get_user_uac(request.user)
    if not chain_store_uac:
        return HttpResponse(json.dumps(response), content_type='application/json')
    term_range = request.GET.get('term_range', WEEKLY)
    store_property = request.GET.get('store_property', 1)
    property_stores_set = set()
    [property_stores_set.add(json.loads(store).get('id')) for store in redisC.smembers('Attr:PROPERTY:%d' % store_property)]
    stores_uac = stores_uac & property_stores_set
    date = get_term_start_date(datetime.date.today(), term_range)
    stores = {}
    [stores.update({json.loads(store).get('id'): json.loads(store)}) for store in redisC.smembers('chainstore_id:%d' % chain_store_uac)]
    for _id in stores.keys():
        if int(_id) not in stores_uac:
            stores.pop(_id)

    while date <= datetime.date.today():
        sales_target_set = redisC.smembers('daily_target:%s:chainstore_id:%s' % (date, chain_store_uac))
        for _row in sales_target_set:
            row = json.loads(_row)
            if int(row.get('id')) in stores_uac:
                if stores.get(row.get('id')).get('sales_target'):
                    stores[row.get('id')]['sales_target'] += 0 if not row.get('sales') else row.get('sales')
                else:
                    stores[row.get('id')]['sales_target'] = 0 if not row.get('sales') else row.get('sales')
        sales_set = redisC.smembers('sales:%s:chainstore_id:%d' % (date, chain_store_uac))
        print 'sales:%s:chainstore_id:%d' % (date, chain_store_uac)
        for _row in sales_set:
            row = json.loads(_row)
            if int(row.get('id')) in stores_uac:
                if stores.get(row.get('id')).get('sales'):
                    stores[row.get('id')]['sales'] += 0 if not row.get('sales') else row.get('sales')
                else:
                    stores[row.get('id')]['sales'] = 0 if not row.get('sales') else row.get('sales')
        gross_profit_set = redisC.smembers('gross_profit:%s:chainstore_id:%s' % (date, chain_store_uac))
        for _row in gross_profit_set:
            row = json.loads(_row)
            if int(row.get('id')) in stores_uac:
                if stores.get(row.get('id')).get('gross_profit'):
                    stores[row.get('id')]['gross_profit'] += 0 if not row.get('gross_profit') else row.get('gross_profit')
                else:
                    stores[row.get('id')]['gross_profit'] = 0 if not row.get('gross_profit') else row.get('gross_profit')
        date += datetime.timedelta(days=1)
    for _id, store in stores.items():
        if store.get('sales') and store.get('gross_profit'):
            stores[_id]['gross_profit_rate'] = store.get('gross_profit') / store.get('sales')
        if store.get('sales') and store.get('sales_target'):
            stores[_id]['difference'] = store.get('sales') - store.get('sales_target')
            stores[_id]['completeness'] = store.get('sales') / store.get('sales_target')
    stores=stores.values()
    print stores
    all_items_count = len(stores)
    all_page_count = divmod(all_items_count, 20)[0] if divmod(all_items_count,20)[1] == 0 else divmod(all_items_count, 20)[0] + 1

    page_list = [i for i in xrange(1, all_page_count + 1)]
    page_list = map(num_to_chinese, page_list)
    current_page = request.GET.get('current_page', '1')
    obj = Pagination(current_page, all_items_count)
    all_response_date = {}
    current_store_list = stores[obj.start:obj.end]
    all_response_date['all_page_count'] = all_page_count
    all_response_date['page_list'] = page_list
    all_response_date['current_store_list'] = current_store_list


    return HttpResponse(json.dumps(all_response_date))
def get_term_end_date(date, term_range):
    _date = date
    if isinstance(date, str):
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    if term_range == TODAY:
        date = date
    elif term_range == YESTERDAY:
        date = date - datetime.timedelta(days=1)
    elif term_range == WEEKLY:
        while date.weekday() != 6:
            date = date + datetime.timedelta(days=1)
    elif term_range == MONTHLY:
        while date != datetime.date(_date.year, _date.month + 1, 1) - datetime.timedelta(days=1):
            date = date + datetime.timedelta(days=1)
    elif term_range == SEASONALLY:
        while date.month not in (3, 6, 9, 12) or date.day not in (30, 31):
            date = date + datetime.timedelta(days=1)
    elif term_range == YEARLY:
        while date.month != 12 or date.day != 31:
            date = date + datetime.timedelta(days=1)
    return date

def overall_chart(term_range,store_property,chain_store_uac,stores_uac):
    property_stores_set = set()
    [property_stores_set.add(json.loads(store).get('id')) for store in redisC.smembers('Attr:PROPERTY:%d' % store_property)]
    stores_uac = stores_uac & property_stores_set
    date = get_term_start_date(datetime.date.today(), term_range)
    end_date = get_term_end_date(datetime.date.today(), term_range)
    stores = {}
    [stores.update({json.loads(store).get('id'): json.loads(store)}) for store in redisC.smembers('chainstore_id:%d' % chain_store_uac)]
    for _id in stores.keys():
        if int(_id) not in stores_uac:
            stores.pop(_id)
    result = {}
    print date, end_date
    while date <= end_date:
        result[str(date)] = {}
        sales_target_set = redisC.smembers('daily_target:%s:chainstore_id:%s' % (date, chain_store_uac))
        for _row in sales_target_set:
            row = json.loads(_row)
            if int(row.get('id')) in stores_uac:
                if not result[str(date)].get('daily_target'):
                    result[str(date)]['daily_target'] = 0 if not row.get('sales') else row.get('sales')
                result[str(date)]['daily_target'] += 0 if not row.get('sales') else row.get('sales')
        sales_set = redisC.smembers('sales:%s:chainstore_id:%s' % (date, chain_store_uac))
        for _row in sales_set:
            row = json.loads(_row)
            if int(row.get('id')) in stores_uac:
                if not result[str(date)].get('sales'):
                    result[str(date)]['sales'] = 0 if not row.get('sales') else row.get('sales')
                result[str(date)]['sales'] += 0 if not row.get('sales') else row.get('sales')
                if not result[str(date)].get('num_trades'):
                    result[str(date)]['num_trades'] = 0 if not row.get('num_trades') else row.get('num_trades')
                result[str(date)]['num_trades'] += 0 if not row.get('num_trades') else row.get('num_trades')
                if not result[str(date)].get('num'):
                    result[str(date)]['num'] = 0 if not row.get('num') else row.get('num')
                result[str(date)]['num'] += 0 if not row.get('num') else row.get('num')
        gross_profit_set = redisC.smembers('gross_profit:%s:chainstore_id:%s' % (date, chain_store_uac))
        for _row in gross_profit_set:
            row = json.loads(_row)
            if int(row.get('id')) in stores_uac:
                if not result[str(date)].get('gross_profit'):
                    result[str(date)]['gross_profit'] = 0 if not row.get('gross_profit') else row.get('gross_profit')
                result[str(date)]['gross_profit'] += 0 if not row.get('gross_profit') else row.get('gross_profit')

        date += datetime.timedelta(days=1)
    result1 = sorted(result.iteritems(), key=lambda d:d[0])
    y={}
    y['sales'] = [item.get('sales') for _, item in tuple(result1)]
    y['num'] = [item.get('num') for _, item in tuple(result1)]
    y['num_trades'] = [item.get('num_trades') for _, item in tuple(result1)]
    y['gross_profit'] = [item.get('gross_profit') for _, item in tuple(result1)]

    return [item for item, _ in tuple(result1)],y

def overall_store_chart(term_range,store_property,chain_store_uac,stores_id):
    property_stores_set = set()
    [property_stores_set.add(json.loads(store).get('id')) for store in redisC.smembers('Attr:PROPERTY:%d' % store_property)]
    stores_uac = property_stores_set
    date = get_term_start_date(datetime.date.today(), term_range)
    end_date = get_term_end_date(datetime.date.today(), term_range)
    stores = {}
    [stores.update({json.loads(store).get('id'): json.loads(store)}) for store in redisC.smembers('chainstore_id:%d' % chain_store_uac)]
    for _id in stores.keys():
        if int(_id) not in stores_uac:
            stores.pop(_id)
    result = {}
    print date, end_date
    while date <= end_date:
        result[str(date)] = {}
        sales_target_set = redisC.smembers('daily_target:%s:chainstore_id:%s' % (date, chain_store_uac))
        for _row in sales_target_set:
            row = json.loads(_row)
            if int(row.get('id')) == stores_uac:
                if not result[str(date)].get('daily_target'):
                    result[str(date)]['daily_target'] = 0 if not row.get('sales') else row.get('sales')
                result[str(date)]['daily_target'] += 0 if not row.get('sales') else row.get('sales')
        sales_set = redisC.smembers('sales:%s:chainstore_id:%s' % (date, chain_store_uac))
        for _row in sales_set:
            row = json.loads(_row)
            if int(row.get('id')) == stores_uac:
                if not result[str(date)].get('sales'):
                    result[str(date)]['sales'] = 0 if not row.get('sales') else row.get('sales')
                result[str(date)]['sales'] += 0 if not row.get('sales') else row.get('sales')
                if not result[str(date)].get('num_trades'):
                    result[str(date)]['num_trades'] = 0 if not row.get('num_trades') else row.get('num_trades')
                result[str(date)]['num_trades'] += 0 if not row.get('num_trades') else row.get('num_trades')
                if not result[str(date)].get('num'):
                    result[str(date)]['num'] = 0 if not row.get('num') else row.get('num')
                result[str(date)]['num'] += 0 if not row.get('num') else row.get('num')
        gross_profit_set = redisC.smembers('gross_profit:%s:chainstore_id:%s' % (date, chain_store_uac))
        for _row in gross_profit_set:
            row = json.loads(_row)
            if int(row.get('id')) == stores_id:
                if not result[str(date)].get('gross_profit'):
                    result[str(date)]['gross_profit'] = 0 if not row.get('gross_profit') else row.get('gross_profit')
                result[str(date)]['gross_profit'] += 0 if not row.get('gross_profit') else row.get('gross_profit')

        date += datetime.timedelta(days=1)
    result1 = sorted(result.iteritems(), key=lambda d:d[0])
    y={}
    y['sales'] = [item.get('sales') for _, item in tuple(result1)]
    y['num'] = [item.get('num') for _, item in tuple(result1)]
    y['num_trades'] = [item.get('num_trades') for _, item in tuple(result1)]
    y['gross_profit'] = [item.get('gross_profit') for _, item in tuple(result1)]

    return [item for item, _ in tuple(result1)],y 

def store_overall_data(request,store_id):
    response = {'success': 0, 'data': {}}
    chain_store_uac, stores_uac, categories_uac, areas = get_user_uac(request.user)
    if not chain_store_uac:
        return HttpResponse(json.dumps(response), content_type='application/json')
    term_range = request.GET.get('date_rule', WEEKLY)

    store_property = request.GET.get('store_property', 1)
    property_stores_set = set()
    [property_stores_set.add(json.loads(store).get('id')) for store in redisC.smembers('Attr:PROPERTY:%d' % store_property)]
    stores_uac =  property_stores_set
    date = get_term_start_date(datetime.date.today(), term_range)
    sales = 0.0
    sales_target = 0.0
    gross_profit = 0.0
    num_trades = 0.0
    num = 0.0
    term_beginning_invnetory = 0.0
    term_end_inventory = 0.0
    term_beginning_invnetory_set = redisC.smembers('inventory:%s:chainstore_id:%d' % (date, chain_store_uac))
    for _row in term_beginning_invnetory_set:
        row = json.loads(_row)
        if int(row.get('id')) == store_id:
            term_beginning_invnetory += 0 if not row.get('quantity_sum') else row.get('quantity_sum')
    term_end_invnetory_set = redisC.smembers('inventory:%s:chainstore_id:%d' % (datetime.date.today() - datetime.timedelta(days=1), chain_store_uac))
    for _row in term_end_invnetory_set:
        row = json.loads(_row)
        if int(row.get('id')) == store_id:
            term_end_inventory += 0 if not row.get('quantity_sum') else row.get('quantity_sum')
    while date <= datetime.date.today():
        sales_target_set = redisC.smembers('daily_target:%s:chainstore_id:%s' % (date, chain_store_uac))
        for _row in sales_target_set:
            row = json.loads(_row)
            if int(row.get('id')) == store_id:
                sales_target += 0 if not row.get('sales') else row.get('sales')
                for _, _area in areas.items():
                    if int(row.get('id')) in _area.get('stores'):
                        if _area.get('sales_target'):
                            areas[_]['sales_target'] += 0 if not row.get('sales') else row.get('sales')
                        else:
                            areas[_]['sales_target'] = 0 if not row.get('sales') else row.get('sales')
        sales_set = redisC.smembers('sales:%s:chainstore_id:%s' % (date, chain_store_uac))
        for _row in sales_set:
            row = json.loads(_row)
            if int(row.get('id')) == store_id:
                sales += 0 if not row.get('sales') else row.get('sales')
                num_trades += 0 if not row.get('num_trades') else row.get('num_trades')
                num += 0 if not row.get('num') else row.get('num')
                for _, _area in areas.items():
                    if int(row.get('id')) in _area.get('stores'):
                        if _area.get('sales'):
                            areas[_]['sales'] += 0 if not row.get('sales') else row.get('sales')
                        else:
                            areas[_]['sales'] = 0 if not row.get('sales') else row.get('sales')
        gross_profit_set = redisC.smembers('gross_profit:%s:chainstore_id:%s' % (date, chain_store_uac))
        for _row in gross_profit_set:
            row = json.loads(_row)
            if int(row.get('id')) == store_id:
                if row.get('gross_profit'):
                    print row.get('gross_profit')
                gross_profit += 0.0 if not row.get('gross_profit') else row.get('gross_profit')
                for _, _area in areas.items():
                    if int(row.get('id')) in _area.get('stores'):
                        if _area.get('gross_profit'):
                            areas[_]['gross_profit'] += 0 if not row.get('gross_profit') else row.get('gross_profit')
                        else:
                            areas[_]['gross_profit'] = 0 if not row.get('gross_profit') else row.get('gross_profit')
        date = date + datetime.timedelta(days=1)
    try:
        inventory_turnover_ratio = num / (term_beginning_invnetory+term_end_inventory) / 2
    except Exception:
        inventory_turnover_ratio=0
    if num_trades!=0:
            trade_unit_price = sales / num_trades 
    else:
        trade_unit_price=0
    difference = sales - sales_target
    if sales!=0:
            gross_profit_rate = gross_profit / sales
    else:
        gross_profit_rate=0
    if sales_target!=0:
            completion_rate = sales / sales_target
    else:
        completion_rate=0
    all_response_date={}
    overall_data={}
    overall_data['tsales']=sales_target
    overall_data['finsh_rate']=completion_rate
    overall_data['balance']=difference
    overall_data['total_turnover']=inventory_turnover_ratio
    overall_data['sales']=sales
    overall_data['gross_profit']=gross_profit
    overall_data['num_trades']=num_trades
    overall_data['each_num_trades_sales']=trade_unit_price
    all_response_date['overall_data']=overall_data
    all_response_date['area_list']=areas.values() 
    all_response_date['X_axis'],all_response_date['Y_axis']=overall_chart(term_range,store_property,chain_store_uac,stores_uac)
    return HttpResponse(json.dumps(all_response_date)) 

def store_items(request):
    response = {'success': 0, 'data': {}}
    chain_store_uac, stores_uac, categories_uac, areas = get_user_uac(request.user)
    if not chain_store_uac:
        return HttpResponse(json.dumps(response), content_type='application/json')
    term_range = request.GET.get('term_range', MONTHLY)
    date = get_term_start_date(datetime.date.today(), term_range)
    store_property = request.GET.get('store_property', 1)
    property_stores_set = set()
    [property_stores_set.add(json.loads(store).get('id')) for store in redisC.smembers('Attr:PROPERTY:%d' % store_property)]
    stores_uac = stores_uac & property_stores_set
    result = {}
    while date <= datetime.date.today():
        store_items_set = redisC.smembers('store_item:%s:chainstore:%d:store:681303' % (date, chain_store_uac))
        for _row in store_items_set:
            row = json.loads(_row)
            if not result.get(row.get('item_id')):
                result[row.get('item_id')] = {}
            if not result.get(row.get('item_id')).get('item_id'):
                result[row.get('item_id')]['item_id'] = row.get('item_id')
            if not result.get(row.get('item_id')).get('state_name'):
                result[row.get('item_id')]['state_name'] = row.get('state_name')
            if not result.get(row.get('item_id')).get('barcode'):
                result[row.get('item_id')]['barcode'] = row.get('barcode')
            if not result.get(row.get('item_id')).get('item_name'):
                result[row.get('item_id')]['item_name'] = row.get('item_name')
            if not result.get(row.get('item_id')).get('unit_price') and row.get('sales') and row.get('num'):
                result[row.get('item_id')]['unit_price'] = row.get('sales') / row.get('num')
            if not result.get(row.get('item_id')).get('gross_profit'):
                result[row.get('item_id')]['gross_profit'] = 0 if not row.get('gross_profit') else row.get('gross_profit')
            result[row.get('item_id')]['gross_profit'] += 0 if not row.get('gross_profit') else row.get('gross_profit')
            if not result.get(row.get('item_id')).get('num'):
                result[row.get('item_id')]['num'] = 0 if not row.get('num') else row.get('num')
            result[row.get('item_id')]['num'] += 0 if not row.get('num') else row.get('num')
            if not result.get(row.get('item_id')).get('sales'):
                result[row.get('item_id')]['sales'] = 0 if not row.get('sales') else row.get('sales')
            result[row.get('item_id')]['sales'] += 0 if not row.get('sales') else row.get('sales')

        date += datetime.timedelta(days=1)

        return HttpResponse(json.dumps(result))
