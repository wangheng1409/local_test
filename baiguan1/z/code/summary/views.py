# -*- coding: utf-8 -*-

from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, HttpResponse
from django.conf import settings
from django.db import connection
from .models import *
from operator import itemgetter
from django.db.models import Count, Sum, F, FloatField
from django.contrib.auth.decorators import login_required

import re
import collections
import datetime
import calendar
import json

from core import choices, sql_utils
from store.models import Store, StoreItem, StoreItemInventory
from .forms import QueryForm
from collections import defaultdict
import pandas

@staff_member_required
def daily_store_category_sales(request, date, store_pk, template='summary/table.html'):
    cursor = connection.cursor()
    vendor_filter = request.GET.get('verec_ddndor', None)
    if vendor_filter:
        vendor = "vendor = '%s'" % vendor_filter
    else:
        vendor = '1 = 1'
    cursor.execute("""

        select sum(sales) as sales, sum(num) as num, category
        from summary_dailystoreitemsummary
        join
            (select barcode from standard_standarditem where standard_standarditem.status = 'human_verified' and %s ) as verified_sku
        on verified_sku.barcode = summary_dailystoreitemsummary.barcode
        where store_id = %s and date = '%s'
        group by category, store_id, date
        order by sales desc;

        """ % (vendor, store_pk, date))
    header = [u'銷售額', u'銷量', u'類別']
    content = []
    for raw_row in cursor.fetchall():
        row = list(raw_row)
        if row[2]:
            row[2] = choices.STANDARD_ITEMS_CATEGORIES_DICT[row[2]]
        content.append(row)

    store = Store.objects.get(pk=store_pk)
    return render(request, template, {'header': header, 'content': content, 'date': date, 'store_name':store.name})

@staff_member_required
def daily_store_category_sales_detail(request, date, store_pk, template='summary/table.html'):

    cursor = connection.cursor()
    cursor.execute("""

        select store_storeitem.id,
               store_storeitem.name,
               standard_standarditem.name,
               summary_dailystoreitemsummary.sales,
               summary_dailystoreitemsummary.num,
               summary_dailystoreitemsummary.category
        from summary_dailystoreitemsummary
            join store_storeitem
            on store_storeitem.id = summary_dailystoreitemsummary.item_id
            left join standard_standarditem
            on standard_standarditem.barcode = summary_dailystoreitemsummary.barcode
        where summary_dailystoreitemsummary.store_id = %s and date = '%s'
        order by sales desc;

        """ % (store_pk, date))
    header = [u'ID', u'商品', u'标准品',  u'銷售額', u'銷量', u'類別']
    content = []
    for raw_row in cursor.fetchall():
        row = list(raw_row)
        if row[5]:
            row[5] = choices.STANDARD_ITEMS_CATEGORIES_DICT[row[5]]
        content.append(row)

    store = Store.objects.get(pk=store_pk)
    return render(request, template, {'header': header, 'content': content, 'date': date, 'store_name':store.name})


@staff_member_required
def monthly_store_category_sales(request, date, store_pk, template='summary/table.html'):
    cursor = connection.cursor()
    vendor_filter = request.GET.get('vendor', None)
    if vendor_filter:
        vendor = "vendor = '%s'" % vendor_filter
    else:
        vendor = '1 = 1'
    cursor.execute("""

        select date, store_id, sum(sales) as sales, sum(num) as num, category
        from summary_monthlystoreitemsummary
        join
            (select barcode from standard_standarditem where standard_standarditem.status = 'human_verified' and %s ) as verified_sku
        on verified_sku.barcode = summary_monthlystoreitemsummary.barcode
        where store_id = %s and date = %s
        group by category, store_id, date
        order by sales desc;

        """ % (vendor, store_pk, date))
    header = [u'日期', u'店', u'銷售額', u'銷量', u'類別']
    content = []
    for row in cursor.fetchall():
        row = list(raw_row)
        row[5] = choices.STANDARD_ITEMS_CATEGORIES_DICT[row[4]]
        content.append(row)

    store = Store.objects.get(pk=store_pk)
    return render(request, template, {'header': header, 'content': content, 'date': date, 'store_name':store.name})


def slice_helper(date, store_pk, vendor_name):
    if vendor_name:
        vendor = "vendor = '%s'" % vendor_name
    else:
        vendor = '1 = 1'

    cursor = connection.cursor()
    cursor.execute("""

        select date, store_id, sum(sales) as sales, sum(num) as num, category
        from summary_monthlystoreitemsummary
        join
            (select barcode from standard_standarditem where standard_standarditem.status = 'human_verified' and %s ) as verified_sku
        on verified_sku.barcode = summary_monthlystoreitemsummary.barcode
        where store_id = %s and date = %s and category is not null
        group by category, store_id, date
        order by sales desc;

        """ % (vendor, store_pk, date))

    return dictfetchall(cursor)

def get_previous_month(date_str):
    tok = date_str.split('-')
    int_month = int(tok[1])
    if int_month == 1:
        return '%d12' % (int(tok[0]) - 1)
    else:
        int_month -= 1
        if int_month < 10:
            return '%s0%d' % (tok[0], int_month)
        return '%s%d' % (tok[0], int_month)


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def to_cat_dict(sales):
    out = {}
    total_sales = 0
    total_num = 0
    for cat in choices.COCACOLA_FOCUS_CATEGORIES.keys():
        out[cat] = {'sales': None, 'num': None, 'sales_percentage': None, 'num_percentage': None}

    for row in sales:
        cat = row['category']
        if cat in choices.COCACOLA_FOCUS_CATEGORIES.keys():
            out[cat]['sales'] = row['sales']
            out[cat]['num'] = row['num']
            total_sales += row['sales']
            total_num += row['num']

    for cat in out.keys():
        if out[cat]['sales']:
            out[cat]['sales_percentage'] = round(out[cat]['sales'] / total_sales * 100.0, 2)
        else:
            out[cat]['sales_percentage'] = None

        if out[cat]['num']:
            out[cat]['num_percentage'] = round(out[cat]['num'] / total_num * 100.0, 2)
        else:
            out[cat]['num_percentage'] = None

    return out

def growth_rate(rate):
    if rate:
        return '+%.2f' % rate if rate > 0 else '%.2f' % rate


def combine_dict(pre, cur):
    out = {}
    for cat in choices.COCACOLA_FOCUS_CATEGORIES.keys():
        if not pre[cat]['sales'] or \
           not pre[cat]['num'] or \
           not pre[cat]['sales_percentage'] or \
           not pre[cat]['num_percentage']:

            out[cat] = {'display_cat': choices.COCACOLA_FOCUS_CATEGORIES[cat],
                        'sales': None,
                        'num': None,
                        'sales_growth': None,
                        'num_growth': None,
                        'sales_percentage': None,
                        'sales_percentage_growth': None
                        }
            if 'sales_percentage_in_overall' in pre[cat] and \
               'sales_percentage_in_overall' in cur[cat]:
                out[cat]['sales_percentage_in_overall'] = None
                out[cat]['sales_percentage_growth_in_overall'] = None
        else:
            g_pt = round((cur[cat]['sales_percentage'] -  pre[cat]['sales_percentage']), 2)
            out[cat] = {'display_cat': choices.COCACOLA_FOCUS_CATEGORIES[cat],
                        'sales': cur[cat]['sales'],
                        'num': cur[cat]['num'],
                        'sales_growth': growth_rate(round((cur[cat]['sales'] -  pre[cat]['sales']) / pre[cat]['sales'] * 100.0, 2)),
                        'num_growth': growth_rate(round((cur[cat]['num'] -  pre[cat]['num']) / pre[cat]['num'] * 100.0, 2)),
                        'sales_percentage': cur[cat]['sales_percentage'],
                        'sales_percentage_growth': growth_rate(g_pt)
                        }
            if 'sales_percentage_in_overall' in pre[cat] and \
               'sales_percentage_in_overall' in cur[cat]:
                out[cat]['sales_percentage_in_overall'] = cur[cat]['sales_percentage_in_overall']
                pt = round(cur[cat]['sales_percentage_in_overall'] - pre[cat]['sales_percentage_in_overall'], 2)
                out[cat]['sales_percentage_growth_in_overall'] = growth_rate(pt)
    return out

def addon_column(vendor, overall):
    for cat in choices.COCACOLA_FOCUS_CATEGORIES.keys():
        if overall[cat]['sales'] == None or vendor[cat]['sales'] == None:
            vendor[cat]['sales_percentage_in_overall'] = None
        else:
            vendor[cat]['sales_percentage_in_overall'] = round(vendor[cat]['sales'] / overall[cat]['sales'] * 100.0, 2)
    return vendor

@staff_member_required
def monthly_store_category_sales_combine(request, date, store_pk, template='summary/combine.html'):

    vendor_name = request.GET.get('vendor', None)
    cur_month = date.replace('-', '')
    pre_month = get_previous_month(date)

    overall_pre = to_cat_dict(slice_helper(pre_month, store_pk, None))
    overall_cur = to_cat_dict(slice_helper(cur_month, store_pk, None))

    vendor_pre = to_cat_dict(slice_helper(pre_month, store_pk, vendor_name))
    vendor_cur = to_cat_dict(slice_helper(cur_month, store_pk, vendor_name))
    vendor_pre = addon_column(vendor_pre, overall_pre)
    vendor_cur = addon_column(vendor_cur, overall_cur)

    overall = combine_dict(overall_pre, overall_cur)
    vendor = combine_dict(vendor_pre, vendor_cur)

    store = Store.objects.get(pk=store_pk)
    return render(request, template, {'overall': overall,
                                       'vendor': vendor,
                                       'vendor_name': vendor_name,
                                       'store_name': store.name,
                                       'date': date})


def vendor_sales_helper(all_sales, overall_sales, cur_month_str, pre_month_str):
    """
        vendor: {'date1': {'sales': x, 'num': y}, 'date2': {'sales': x, 'num': y}}
    """
    out = {}
    vendors = {}
    cur_month = int(cur_month_str)
    pre_month = int(pre_month_str)
    for s in all_sales:
        if s['vendor'] not in vendors:
            vendors[s['vendor']] = {cur_month: {'sales': 0, 'num': 0}, pre_month: {'sales': 0, 'num':0}}
        vendors[s['vendor']][s['date']] = {'sales': s['sales'], 'num': s['num']}

    overall_sales_dict = {}
    for s in overall_sales:
        overall_sales_dict[s['date']] = s['sales']


    for vendor, values in vendors.items():
        if not values[pre_month]['sales']:
            sales_growth = 0
        else:
            sales_growth = growth_rate(round((values[cur_month]['sales'] - values[pre_month]['sales']) / values[pre_month]['sales']  * 100.0, 2))
        out[vendor] = {'vendor': vendor, \
                      'sales': values[cur_month]['sales'], \
                       'sales_growth': sales_growth, \
                       'sales_percentage_in_overall': round(values[cur_month]['sales'] / overall_sales_dict[cur_month] * 100.0, 2), \
                       'sales_percentage_growth_in_overall': growth_rate(round(values[cur_month]['sales'] / overall_sales_dict[cur_month] * 100.0, 2) - round(values[pre_month]['sales'] / overall_sales_dict[pre_month] * 100.0, 2))
                      }
    return out

@staff_member_required
def monthly_store_category_sales_vendor_rank(request, date, store_pk, template='summary/store_vendor_rank.html'):
    vendors = request.GET.getlist('vendors', None)
    category = request.GET.get('category', None)

    store = Store.objects.get(pk=store_pk)
    vendor_sql = ' or '.join(["vendor = '%s'" % v for v in vendors])
    if vendor_sql:
        vendors_final = vendor_sql
    else:
        vendors_final = '1=1'

    cur_month = date.replace('-', '')
    pre_month = get_previous_month(date)

    if category and category in choices.COCACOLA_FOCUS_CATEGORIES:
        categories = "category = '%s'" % category
    else:
        categories = ' or '.join(["category = '%s'" % c for c in choices.COCACOLA_FOCUS_CATEGORIES.keys()])

    cursor = connection.cursor()
    cursor.execute("""
        select date, sum(sales) as sales, sum(num) as num, verified_sku.vendor
        from summary_monthlystoreitemsummary
        join
            (select barcode, vendor from standard_standarditem
             where standard_standarditem.status = 'human_verified' and
                (%s) and (%s)
            ) as verified_sku
        on verified_sku.barcode = summary_monthlystoreitemsummary.barcode
        where store_id = %s and (date = '%s' or date = '%s')
        group by vendor, date;
    """ % (categories, vendors_final, store_pk, pre_month, cur_month))
    all_sales = dictfetchall(cursor)

    cursor = connection.cursor()
    cursor.execute("""
        select date, sum(sales) as sales, sum(num) as num
        from summary_monthlystoreitemsummary
        join
            (select barcode, vendor from standard_standarditem
             where standard_standarditem.status = 'human_verified' and
                  (%s)
            ) as verified_sku
        on verified_sku.barcode = summary_monthlystoreitemsummary.barcode
        where store_id = %s and (date = '%s' or date = '%s')
        group by date;
        """ % (categories, store_pk, pre_month, cur_month))

    overall_sales = dictfetchall(cursor)
    result_dict = vendor_sales_helper(all_sales, overall_sales, cur_month, pre_month)
    result = sorted(result_dict.values(), key = itemgetter('sales'), reverse=True)
    return render(request, template, {'store_name': store.name, 'date': date, 'result': result, 'category': choices.COCACOLA_FOCUS_CATEGORIES[category] if category else None})

# models = set(['CAN', 'PET SS', 'PET 601-1999ml', '2L', '2L+'])
models = ['<400ml', '400-600ml', '601-1999ml', '2000ml', '2000ml+']
def model_mapper(model):
    """
        -- can - <400ml
        -- PET SS - 400 - 600ml
        -- PET 601-1999mL - 1250ml 1000ml, 2000ml
        -- 2L
        -- 2L+
    """
    p = re.search(r'(\d+)(\*\d+)*', model)
    if p:
        raw_model = int(p.group(1))
        # raw_model = int(model.replace('ml', ''))
        if raw_model < 400:
            return '<400ml'
        elif raw_model <= 600:
            return '400-600ml'
        elif raw_model < 2000:
            return '601-1999ml'
        elif raw_model == 2000:
            return '2000ml'
        # elif raw_model < 10000:
        else:
            return '2000ml+'

    # print model
    # print raw_model
    # return 'OTHERS'


def sales_vendor_model_helper(all_sales, overall_sales, cur_month_str, pre_month_str):
    """
        vendor: {'date1': {'model': {'sales': x, 'num': y}, 'date2': {'sales': x, 'num': y}}
    """
    vendors = {}
    cur_month = int(cur_month_str)
    pre_month = int(pre_month_str)

    # compute partial result
    for s in all_sales:
        if s['vendor'] not in vendors:
            vendors[s['vendor']] = {cur_month: {}, pre_month: {}}
            for mi in models:
                vendors[s['vendor']][pre_month][mi] = 0
                vendors[s['vendor']][cur_month][mi] = 0
        m = model_mapper(s['model'])
        if not m:
            print s['model']
        else:
            vendors[s['vendor']][s['date']][m] += s['sales']

    ## init overall_sales
    overall_sales_dict = {pre_month:{}, cur_month:{}}
    for mi in models:
        overall_sales_dict[pre_month][mi] = 0
        overall_sales_dict[cur_month][mi] = 0

    for s in overall_sales:
        m = model_mapper(s['model'])
        overall_sales_dict[s['date']][m] += s['sales']

    # compute final result
    out = {}
    for vendor, values in vendors.items():
        if vendor not in out:
            out[vendor] = collections.OrderedDict()

        for mi in models:
            if not values[pre_month][mi]:
                sales_growth = 0.0
            else:
                sales_growth = growth_rate(round((values[cur_month][mi] - values[pre_month][mi]) / values[pre_month][mi]  * 100.0, 2))
            if mi not in out[vendor]:
                out[vendor][mi] = {}

            if not overall_sales_dict[cur_month][mi]:
                cur_sales_percentage_in_overall = 0.0
            else:
                cur_sales_percentage_in_overall = round(values[cur_month][mi] / overall_sales_dict[cur_month][mi] * 100.0, 2)

            if not overall_sales_dict[pre_month][mi]:
                pre_sales_percentage_in_overall = 0.0
            else:
                pre_sales_percentage_in_overall = round(values[pre_month][mi] / overall_sales_dict[pre_month][mi] * 100.0, 2)

            out[vendor][mi] = {'vendor': vendor, \
                               'model': mi, \
                               'sales': values[cur_month][mi], \
                               'sales_growth': sales_growth, \
                               'sales_percentage_in_overall': cur_sales_percentage_in_overall, \
                               'sales_percentage_growth_in_overall': growth_rate(cur_sales_percentage_in_overall - pre_sales_percentage_in_overall), \
                              }
    return out

@staff_member_required
def monthly_store_category_sales_vendor_model(request, date, store_pk, template='summary/vendor_model.html'):
    vendors = request.GET.getlist('vendors', None)
    category = request.GET.get('category', None)

    store = Store.objects.get(pk=store_pk)
    vendor_sql = ' or '.join(["vendor = '%s'" % v for v in vendors])
    if vendor_sql:
        vendors_final = vendor_sql
    else:
        vendors_final = '1=1'

    cur_month = date.replace('-', '')
    pre_month = get_previous_month(date)

    if category and category in choices.COCACOLA_FOCUS_CATEGORIES:
        categories = "category = '%s'" % category
    else:
        categories = ' or '.join(["category = '%s'" % c for c in choices.COCACOLA_FOCUS_CATEGORIES.keys()])

    cursor = connection.cursor()
    cursor.execute("""
        select date, model, sum(sales) as sales, sum(num) as num, verified_sku.vendor
        from summary_monthlystoreitemsummary
        join
            (select barcode, vendor from standard_standarditem
             where standard_standarditem.status = 'human_verified' and
                (%s) and (%s)
            ) as verified_sku
        on verified_sku.barcode = summary_monthlystoreitemsummary.barcode
        where store_id = %s and (date = '%s' or date = '%s')
        group by vendor, date, model;
    """ % (categories, vendors_final, store_pk, pre_month, cur_month))
    all_sales = dictfetchall(cursor)

    cursor = connection.cursor()
    cursor.execute("""
        select date, model, sum(sales) as sales, sum(num) as num
        from summary_monthlystoreitemsummary
        join
            (select barcode, vendor from standard_standarditem
             where standard_standarditem.status = 'human_verified' and
                  (%s)
            ) as verified_sku
        on verified_sku.barcode = summary_monthlystoreitemsummary.barcode
        where store_id = %s and (date = '%s' or date = '%s')
        group by date, model;
        """ % (categories, store_pk, pre_month, cur_month))

    overall_sales = dictfetchall(cursor)
    result = sales_vendor_model_helper(all_sales, overall_sales, cur_month, pre_month)
    return render(request, template, {'store_name': store.name, 'date': date, 'result': result, 'category': choices.COCACOLA_FOCUS_CATEGORIES[category] if category else None})

def sales_model_vendor_brand_helper(all_sales, overall_sales, cur_month_str, pre_month_str):
    """
        model: {'date1': {'brand1': {'sales': x, 'num': y}, 'brand2': xxx, 'brand3': xxx}, 'date2': ...}
    """
    models_dict = collections.OrderedDict()
    brands = set([b['brand'] for b in all_sales])
    cur_month = int(cur_month_str)
    pre_month = int(pre_month_str)

    for mi in models:
        models_dict[mi] = {cur_month:{}, pre_month:{}}
        for b in brands:
            models_dict[mi][cur_month][b] = 0
            models_dict[mi][pre_month][b] = 0

    # compute partial result
    for s in all_sales:
        m = model_mapper(s['model'])
        models_dict[m][s['date']][s['brand']] += s['sales']

    ## init overall_sales
    overall_sales_dict = {pre_month:{}, cur_month:{}}
    for mi in models:
        overall_sales_dict[pre_month][mi] = 0
        overall_sales_dict[cur_month][mi] = 0

    for s in overall_sales:
        m = model_mapper(s['model'])
        overall_sales_dict[s['date']][m] += s['sales']

    # compute final result
    out = collections.OrderedDict()
    for model, values in models_dict.items():
        if model not in out:
            out[model] = collections.OrderedDict()

        for b in brands:
            if not values[pre_month][b]:
                sales_growth = 0.0
            else:
                sales_growth = growth_rate(round((values[cur_month][b] - values[pre_month][b]) / values[pre_month][b]  * 100.0, 2))
            if b not in out[model]:
                out[model][b] = {}

            if not overall_sales_dict[cur_month][model]:
                cur_sales_percentage_in_overall = 0.0
            else:
                cur_sales_percentage_in_overall = round(values[cur_month][b] / overall_sales_dict[cur_month][model] * 100.0, 2)

            if not overall_sales_dict[pre_month][model]:
                pre_sales_percentage_in_overall = 0.0
            else:
                pre_sales_percentage_in_overall = round(values[pre_month][b] / overall_sales_dict[pre_month][model] * 100.0, 2)

            out[model][b] = {'model': model, \
                             'brand': b, \
                             'sales': values[cur_month][b], \
                             'sales_growth': sales_growth, \
                             'sales_percentage_in_overall': cur_sales_percentage_in_overall, \
                             'sales_percentage_growth_in_overall': growth_rate(cur_sales_percentage_in_overall - pre_sales_percentage_in_overall), \
                              }
    return out

@staff_member_required
def monthly_store_category_sales_model_brand(request, date, store_pk, template='summary/model_brand.html'):
    vendors = request.GET.getlist('vendors', None)
    category = request.GET.get('category', None)

    store = Store.objects.get(pk=store_pk)
    vendor_sql = ' or '.join(["vendor = '%s'" % v for v in vendors])
    if vendor_sql:
        vendors_final = vendor_sql
    else:
        vendors_final = '1=1'

    cur_month = date.replace('-', '')
    pre_month = get_previous_month(date)

    if category and category in choices.COCACOLA_FOCUS_CATEGORIES:
        categories = "category = '%s'" % category
    else:
        categories = ' or '.join(["category = '%s'" % c for c in choices.COCACOLA_FOCUS_CATEGORIES.keys()])

    cursor = connection.cursor()
    cursor.execute("""
        select date, model, sum(sales) as sales, sum(num) as num, verified_sku.brand
        from summary_monthlystoreitemsummary
        join
            (select barcode, brand from standard_standarditem
             where standard_standarditem.status = 'human_verified' and
                (%s) and (%s)
            ) as verified_sku
        on verified_sku.barcode = summary_monthlystoreitemsummary.barcode
        where store_id = %s and (date = '%s' or date = '%s')
        group by brand, date, model;
    """ % (categories, vendors_final, store_pk, pre_month, cur_month))
    all_sales = dictfetchall(cursor)

    cursor = connection.cursor()
    cursor.execute("""
        select date, model, sum(sales) as sales, sum(num) as num
        from summary_monthlystoreitemsummary
        join
            (select barcode from standard_standarditem
             where standard_standarditem.status = 'human_verified' and
                  (%s)
            ) as verified_sku
        on verified_sku.barcode = summary_monthlystoreitemsummary.barcode
        where store_id = %s and (date = '%s' or date = '%s')
        group by date, model;
        """ % (categories, store_pk, pre_month, cur_month))

    overall_sales = dictfetchall(cursor)
    result = sales_model_vendor_brand_helper(all_sales, overall_sales, cur_month, pre_month)
    return render(request, template, {'store_name': store.name, 'date': date, 'result': result, 'category': choices.COCACOLA_FOCUS_CATEGORIES[category] if category else None})

flavors = [u'橙', u'葡萄', u'桃', u'梨', u'热带果粒', u'柠檬', u'其他口味']
def flavor_mapper(f):
    if f in flavors:
        return f
    return u'其他口味'

def sales_model_vendor_model_flavor_helper(all_sales, overall_sales, cur_month_str, pre_month_str):
    """
        vendor: {'date1': {'model1': {'flavor1': sale1, 'flavor2': sale2}, 'model2': {}}, 'date2': {}}
    """
    vendors = {}
    cur_month = int(cur_month_str)
    pre_month = int(pre_month_str)

    # compute partial result
    for s in all_sales:
        if s['vendor'] not in vendors:
            vendors[s['vendor']] = {cur_month: {}, pre_month: {}}
            for mi in models:
                vendors[s['vendor']][pre_month][mi] = {}
                vendors[s['vendor']][cur_month][mi] = {}
                for f in flavors:
                    vendors[s['vendor']][pre_month][mi][f] = 0
                    vendors[s['vendor']][cur_month][mi][f] = 0

        m = model_mapper(s['model'])
        vendors[s['vendor']][s['date']][m][flavor_mapper(s['flavor'])] += s['sales']

    ## init overall_sales
    overall_sales_dict = {pre_month:{}, cur_month:{}}
    for mi in models:
        overall_sales_dict[pre_month][mi] = {}
        overall_sales_dict[cur_month][mi] = {}
        for f in flavors:
            overall_sales_dict[pre_month][mi][f] = 0
            overall_sales_dict[cur_month][mi][f] = 0

    for s in overall_sales:
        m = model_mapper(s['model'])
        overall_sales_dict[s['date']][m][flavor_mapper(s['flavor'])] += s['sales']

    # compute final result
    out = {}
    for vendor, values in vendors.items():
        if vendor not in out:
            out[vendor] = collections.OrderedDict()
        for mi in models:
            out[vendor][mi] = collections.OrderedDict()
            for f in flavors:
                if not values[pre_month][mi][f]:
                    sales_growth = 0.0
                else:
                    sales_growth = growth_rate(round((values[cur_month][mi][f] - values[pre_month][mi][f]) / values[pre_month][mi][f]  * 100.0, 2))

                # if mi not in out[vendor]:
                #     out[vendor][mi] = {f:{}}

                if not overall_sales_dict[cur_month][mi][f]:
                    cur_sales_percentage_in_overall = 0.0
                else:
                    cur_sales_percentage_in_overall = round(values[cur_month][mi][f] / overall_sales_dict[cur_month][mi][f] * 100.0, 2)

                if not overall_sales_dict[pre_month][mi][f]:
                    pre_sales_percentage_in_overall = 0.0
                else:
                    pre_sales_percentage_in_overall = round(values[pre_month][mi][f] / overall_sales_dict[pre_month][mi][f] * 100.0, 2)

                out[vendor][mi][f] = {'vendor': vendor, \
                                       'model': mi, \
                                       'flavor': f, \
                                       'sales': values[cur_month][mi][f], \
                                       'sales_growth': sales_growth, \
                                       'sales_percentage_in_overall': cur_sales_percentage_in_overall, \
                                       'sales_percentage_growth_in_overall': growth_rate(cur_sales_percentage_in_overall - pre_sales_percentage_in_overall), \
                                      }
    return out

@staff_member_required
def monthly_store_sales_vendor_model_flavor(request, date, store_pk, template='summary/vendor_flavor.html'):
    vendors = request.GET.getlist('vendors', None)
    category = request.GET.get('category', None)
    # model = request.GET.get('model', None)

    store = Store.objects.get(pk=store_pk)
    vendor_sql = ' or '.join(["vendor = '%s'" % v for v in vendors])
    if vendor_sql:
        vendors_final = vendor_sql
    else:
        vendors_final = '1=1'

    cur_month = date.replace('-', '')
    pre_month = get_previous_month(date)

    # if model:
    #     model_sql = "model >= '%s' and model <= '%s'" % tuple(model.split('-'))
    # else:
    #     model_sql = '1=1'


    if category and category in choices.COCACOLA_FOCUS_CATEGORIES:
        categories = "category = '%s'" % category
    else:
        categories = ' or '.join(["category = '%s'" % c for c in choices.COCACOLA_FOCUS_CATEGORIES.keys()])

    cursor = connection.cursor()
    cursor.execute("""
        select date, model, sum(sales) as sales, sum(num) as num, flavor, verified_sku.vendor
        from summary_monthlystoreitemsummary
        join
            (select barcode, vendor from standard_standarditem
             where standard_standarditem.status = 'human_verified' and
                (%s) and (%s)
            ) as verified_sku
        on verified_sku.barcode = summary_monthlystoreitemsummary.barcode
        where store_id = %s and (date = '%s' or date = '%s')
        group by flavor, date, model, verified_sku.vendor;
    """ % (categories, vendors_final, store_pk, pre_month, cur_month))
    all_sales = dictfetchall(cursor)

    cursor = connection.cursor()
    cursor.execute("""
        select date, model, sum(sales) as sales, sum(num) as num, flavor
        from summary_monthlystoreitemsummary
        join
            (select barcode from standard_standarditem
             where standard_standarditem.status = 'human_verified' and
                  (%s)
            ) as verified_sku
        on verified_sku.barcode = summary_monthlystoreitemsummary.barcode
        where store_id = %s and (date = '%s' or date = '%s')
        group by flavor, date, model;
        """ % (categories, store_pk, pre_month, cur_month))

    overall_sales = dictfetchall(cursor)
    result = sales_model_vendor_model_flavor_helper(all_sales, overall_sales, cur_month, pre_month)
    return render(request, template, {'store_name': store.name, 'date': date, 'result': result, 'category': choices.COCACOLA_FOCUS_CATEGORIES[category] if category else None})

def last_month(date_str):
    tok = date_str.split('-')
    int_month = int(tok[1])
    if int_month == 1:
        return '%d12' % (int(tok[0]) - 1)
    else:
        int_month -= 1
        if int_month < 10:
            return '%s-0%d' % (tok[0], int_month)
        return '%s-%d' % (tok[0], int_month)

def home(request, template='summary/cocacola.html'):
    this_month = datetime.datetime.today().strftime('%Y-%m')
    urls = [{'name': u'供应商份额表',           'url': u'%s?vendor=可口可乐' % reverse('summary-monthly-category-sales-combine', kwargs={'date': last_month(this_month)})},
            {'name': u'供应商销售额排名',        'url': u'%s?vendors=可口可乐&vendors=百事&vendors=康师傅&vendors=汇源&vendors=农夫山泉&vendors=统一' % reverse('summary-monthly-category-sales-vendor-rank', kwargs={'date': last_month(this_month)})},
            {'name': u'供应商销类别售额排名',     'url': u'%s?category=soft_drinks' % reverse('summary-monthly-category-sales-vendor-rank', kwargs={'date': last_month(this_month)})},
            {'name': u'供应商-包装份额表',       'url': u'%s?vendors=可口可乐&vendors=百事&vendors=康师傅' % reverse('summary-monthly-category-sales-vendor-model', kwargs={'date': last_month(this_month)})},
            {'name': u'包装-供应商份额表',       'url': u'%s?vendors=可口可乐&vendors=百事&category=soft_drinks' % reverse('summary-monthly-category-sales-model-brand', kwargs={'date': last_month(this_month)})},
            {'name': u'供应商-包装-口味份额表',  'url': u'%s?vendors=可口可乐&vendors=康师傅&category=other_drinks' % reverse('summary-monthly-sales-vendor-model-flavor', kwargs={'date': last_month(this_month)})},
            ]

    new_products_testing_urls = [
        {'name': u'雪碧激柠青柠味 vs 雪碧',
         'url':  u'%s?barcodes=6954767436371&barcodes=6954767434674' % reverse('new-products-home')},

        {'name': u'统一ALKAQUA爱夸水 vs 恒大冰泉 vs 百岁山',
         'url':  u'%s?barcodes=6922255447833&barcodes=6925303721695&barcodes=6925303722890&barcodes=6943052100110' % reverse('new-products-home')},

        {'name': u'农夫山泉茶π',
         'url':  u'%s?barcodes=6921168593552&barcodes=6921168593569&barcodes=6921168593583&barcodes=6921168593376' % reverse('new-products-home')},

        {'name': u'统一海之言',
         'url':  u'%s?barcodes=6925303754112&barcodes=6925303754259&barcodes=6925303754495&barcodes=6925303755584&barcodes=6925303755560&barcodes=6925303755591' % reverse('new-products-home')},

        {'name': u'统一海之言柠檬味 vs 乐百氏脉动青柠口味',
         'url':  u'%s?barcodes=6925303754112&barcodes=6902538004045' % reverse('new-products-home')},

        {'name': u'农夫乌龙茶 vs 三得利乌龙茶',
         'url':  u'%s?barcodes=6921168558032&barcodes=6921581596048' % reverse('new-products-home')},
    ]

    return render(request, template, {'urls': urls, 'new_products_testing_urls': new_products_testing_urls})

def by_month_summary(request, date):
    return redirect('%s?vendor=%s' % (reverse('summary-monthly-store-category-sales-combine', kwargs={'date': date, 'store_pk': 14}), u'可口可乐'))

def by_month_summary_detail(request, date, template='summary/store_list.html'):
    return render(request, template)




#########################################################################################################
#########################################################################################################
#########################################################################################################
#########################################################################################################
#########################################################################################################
def summary_params_helper(request):
    vendors = request.GET.getlist('vendors', None)
    category = request.GET.get('category', None)

    if vendors:
        vendor_sql = ' or '.join(["vendor = '%s'" % v for v in vendors])
    else:
        vendor_sql = '1=1'

    if category:
        # category_name = choices.COCACOLA_FOCUS_CATEGORIES[category]
        category_name = None
        category_sql = "category_id = '%s'" % category
    else:
        # category_sql = ' or '.join(["category = '%s'" % c for c in choices.COCACOLA_FOCUS_CATEGORIES.keys()])
        category_sql = '1=1'
        category_name = None

    store_pk = request.GET.get('store_pk', None)
    if store_pk:
        store_sql = "store_id = '%s'" % store_pk
        store = Store.objects.get(pk=store_pk)
        store_name = store.name
    else:
        store_sql = '1=1'
        store_name = None

    return vendor_sql, category_sql, store_sql, store_name, category_name

def args_helper(request):
    # args = []
    # for k, v in request.GET.items():
    #     args.append('%s=%s' % (k,v))
    # return '&'.join(args)
    return ''

@staff_member_required
def monthly_store_list(request, date, template='summary/store_list.html'):
    mode = request.GET.get('mode', None)

    vendor_sql, category_sql, store_sql, store_name, category_name = summary_params_helper(request)
    cur_month = date.replace('-', '')
    pre_month = get_previous_month(date)

    cursor = connection.cursor()
    cursor.execute("""
        select store_id, store_store.name, store_store.lng, store_store.lat
        from summary_monthlystoreitemsummary
        join
            (select barcode, vendor from standard_standarditem
             where standard_standarditem.status = 'human_verified' and
                  (%s)
            ) as verified_sku
            on verified_sku.barcode = summary_monthlystoreitemsummary.barcode
        join store_store
            on store_id = store_store.id
        where (date = '%s' or date = '%s')
        group by store_id, store_store.name, store_store.lng, store_store.lat
    """ % (category_sql, pre_month, cur_month))
    stores = dictfetchall(cursor)

    urls = []
    for s in stores:
        if not mode:
            urls.append({'name': s['name'], 'url': '%s?k=1&%s' % (
                    reverse('summary-monthly-store-category-sales-vendor-rank', kwargs={'date': date, 'store_pk': s['store_id']}),
                    args_helper(request))
                    })
        else:
            if mode == 'combine':
                urls.append({'name': s['name'], 'url': '%s?k=1&%s' % (
                    reverse('summary-monthly-store-category-sales-combine', kwargs={'date': date, 'store_pk': s['store_id']}),
                    args_helper(request))
                    })
            elif mode == 'vendor-rank':
                urls.append({'name': s['name'], 'url': '%s?k=1&%s' % (
                    reverse('summary-monthly-store-category-sales-vendor-rank', kwargs={'date': date, 'store_pk': s['store_id']}),
                    args_helper(request))
                    })
            elif mode == 'vendor-model':
                urls.append({'name': s['name'], 'url': '%s?k=1&%s' % (
                    reverse('summary-monthly-store-category-sales-vendor-model', kwargs={'date': date, 'store_pk': s['store_id']}),
                    args_helper(request))
                    })
            elif mode == 'model-brand':
                urls.append({'name': s['name'], 'url': '%s?k=1&%s' % (
                    reverse('summary-monthly-store-category-sales-model-brand', kwargs={'date': date, 'store_pk': s['store_id']}),
                    args_helper(request))
                    })
            elif mode == 'vendor-flavor':
                urls.append({'name': s['name'], 'url': '%s?k=1&%s' % (
                    reverse('summary-monthly-store-sales-vendor-model-flavor', kwargs={'date': date, 'store_pk': s['store_id']}),
                    args_helper(request))
                    })

    return render(request, template, {'urls': urls})

@staff_member_required
def monthly_category_sales_vendor_rank(request, date, template='summary/vendor_rank.html'):
    vendor_sql, category_sql, store_sql, store_name, category_name = summary_params_helper(request)
    cur_month = date.replace('-', '')
    pre_month = get_previous_month(date)

    cursor = connection.cursor()
    cursor.execute("""
        select date, sum(sales) as sales, sum(num) as num, verified_sku.vendor
        from summary_monthlystoreitemsummary
        join
            (select barcode, vendor from standard_standarditem
             where standard_standarditem.status = 'human_verified' and
                (%s) and (%s)
            ) as verified_sku
        on verified_sku.barcode = summary_monthlystoreitemsummary.barcode
        where (%s) and (date = '%s' or date = '%s')
        group by vendor, date;
    """ % (category_sql, vendor_sql, store_sql, pre_month, cur_month))
    all_sales = dictfetchall(cursor)

    cursor = connection.cursor()
    cursor.execute("""
        select date, sum(sales) as sales, sum(num) as num
        from summary_monthlystoreitemsummary
        join
            (select barcode, vendor from standard_standarditem
             where standard_standarditem.status = 'human_verified' and
                  (%s)
            ) as verified_sku
        on verified_sku.barcode = summary_monthlystoreitemsummary.barcode
        where (%s) and (date = '%s' or date = '%s')
        group by date;
        """ % (category_sql, store_sql, pre_month, cur_month))

    overall_sales = dictfetchall(cursor)
    result_dict = vendor_sales_helper(all_sales, overall_sales, cur_month, pre_month)
    result = sorted(result_dict.values(), key = itemgetter('sales'), reverse=True)

    if not store_name:
        cursor = connection.cursor()
        cursor.execute("""
            select count(distinct store_id) as total_store
            from summary_monthlystoreitemsummary
            join
                (select barcode, vendor from standard_standarditem
                 where standard_standarditem.status = 'human_verified' and
                      (%s)
                ) as verified_sku
            on verified_sku.barcode = summary_monthlystoreitemsummary.barcode
            where (date = '%s' or date = '%s');
        """ % (category_sql, pre_month, cur_month))
        total_store = dictfetchall(cursor)[0]['total_store']
    else:
        total_store = None

    cursor = connection.cursor()
    cursor.execute("""
        select sum(num_trades) as total from summary_monthlystoresummary
        where %s
    """ % store_sql)
    num_trades = int(dictfetchall(cursor)[0]['total'])

    return render(request, template, {'num_trades': num_trades, 'num_store': total_store, 'store_name': store_name, 'date': date, 'result': result, 'category': category_name, 'args': args_helper(request)})

def market_vendor_helper(sales, month):
    out = []
    for s in sales:
        if str(s['date']) == month:
            out.append(s)
    return out

@staff_member_required
def monthly_category_sales_combine(request, date, template='summary/combine2.html'):
    vendor_sql, category_sql, store_sql, store_name, category_name = summary_params_helper(request)
    cur_month = date.replace('-', '')
    pre_month = get_previous_month(date)

    # one vendor
    vendor_name = request.GET.get('vendor', None)
    if vendor_name:
        vendor_sql = "vendor = '%s'" % vendor_name
    else:
        return render(request, template, {'error': 'please input a vendor'})

    cursor = connection.cursor()
    cursor.execute("""
        select date, sum(sales) as sales, sum(num) as num, category
        from summary_monthlystoreitemsummary
        join
            (select barcode, vendor from standard_standarditem
             where standard_standarditem.status = 'human_verified' and
                (%s)
            ) as verified_sku
        on verified_sku.barcode = summary_monthlystoreitemsummary.barcode
        where (date = '%s' or date = '%s')
        group by date, category
    """ % (vendor_sql, pre_month, cur_month))
    vendor_sales = dictfetchall(cursor)

    cursor = connection.cursor()
    cursor.execute("""
        select date, sum(sales) as sales, sum(num) as num, category
        from summary_monthlystoreitemsummary
        join
            (select barcode, vendor from standard_standarditem
             where standard_standarditem.status = 'human_verified'
            ) as verified_sku
        on verified_sku.barcode = summary_monthlystoreitemsummary.barcode
        where (date = '%s' or date = '%s') and category is not null
        group by category, date;
    """ % (pre_month, cur_month))

    overall_sales = dictfetchall(cursor)

    overall_pre = to_cat_dict(market_vendor_helper(overall_sales, pre_month))
    overall_cur = to_cat_dict(market_vendor_helper(overall_sales, cur_month))

    vendor_pre = to_cat_dict(market_vendor_helper(vendor_sales, pre_month))
    vendor_cur = to_cat_dict(market_vendor_helper(vendor_sales, cur_month))
    vendor_pre = addon_column(vendor_pre, overall_pre)
    vendor_cur = addon_column(vendor_cur, overall_cur)

    overall = combine_dict(overall_pre, overall_cur)
    vendor = combine_dict(vendor_pre, vendor_cur)

    if not store_name:
        cursor = connection.cursor()
        cursor.execute("""
            select count(distinct store_id) as total_store
            from summary_monthlystoreitemsummary
            join
                (select barcode, vendor from standard_standarditem
                 where standard_standarditem.status = 'human_verified' and
                      (%s)
                ) as verified_sku
            on verified_sku.barcode = summary_monthlystoreitemsummary.barcode
            where (date = '%s' or date = '%s');
        """ % (category_sql, pre_month, cur_month))
        total_store = dictfetchall(cursor)[0]['total_store']
    else:
        total_store = None

    cursor = connection.cursor()
    cursor.execute("""
        select sum(num_trades) as total from summary_monthlystoresummary
        where %s
    """ % store_sql)
    num_trades = int(dictfetchall(cursor)[0]['total'])

    return render(request, template, {'num_trades': num_trades, 'num_store': total_store, 'store_name': store_name, 'date': date, 'category': category_name, \
                                      'overall': overall, 'vendor':vendor, 'vendor_name': vendor_name})

@staff_member_required
def monthly_category_sales_vendor_model(request, date, template='summary/vendor_model.html'):
    vendor_sql, category_sql, store_sql, store_name, category_name = summary_params_helper(request)
    cur_month = date.replace('-', '')
    pre_month = get_previous_month(date)

    cursor = connection.cursor()
    cursor.execute("""
        select date, model, sum(sales) as sales, sum(num) as num, verified_sku.vendor
        from summary_monthlystoreitemsummary
        join
            (select barcode, vendor from standard_standarditem
             where standard_standarditem.status = 'human_verified' and
                (%s) and (%s)
            ) as verified_sku
        on verified_sku.barcode = summary_monthlystoreitemsummary.barcode
        where (%s) and (date = '%s' or date = '%s')
        group by vendor, date, model;
    """ % (category_sql, vendor_sql, store_sql, pre_month, cur_month))
    all_sales = dictfetchall(cursor)

    cursor = connection.cursor()
    cursor.execute("""
        select date, model, sum(sales) as sales, sum(num) as num
        from summary_monthlystoreitemsummary
        join
            (select barcode, vendor from standard_standarditem
             where standard_standarditem.status = 'human_verified' and
                  (%s)
            ) as verified_sku
        on verified_sku.barcode = summary_monthlystoreitemsummary.barcode
        where (%s) and (date = '%s' or date = '%s') and model <> ''
        group by date, model;
        """ % (category_sql, store_sql, pre_month, cur_month))

    overall_sales = dictfetchall(cursor)
    result = sales_vendor_model_helper(all_sales, overall_sales, cur_month, pre_month)

    if not store_name:
        cursor = connection.cursor()
        cursor.execute("""
            select count(distinct store_id) as total_store
            from summary_monthlystoreitemsummary
            join
                (select barcode, vendor from standard_standarditem
                 where standard_standarditem.status = 'human_verified' and
                      (%s)
                ) as verified_sku
            on verified_sku.barcode = summary_monthlystoreitemsummary.barcode
            where (date = '%s' or date = '%s');
        """ % (category_sql, pre_month, cur_month))
        total_store = dictfetchall(cursor)[0]['total_store']
    else:
        total_store = None

    cursor = connection.cursor()
    cursor.execute("""
        select sum(num_trades) as total from summary_monthlystoresummary
        where %s
    """ % store_sql)
    num_trades = int(dictfetchall(cursor)[0]['total'])

    return render(request, template, {'num_trades': num_trades, 'num_store': total_store, 'store_name': store_name, 'date': date, 'result': result, 'category': category_name})

@staff_member_required
def monthly_category_sales_model_brand(request, date, template='summary/model_brand.html'):
    vendor_sql, category_sql, store_sql, store_name, category_name = summary_params_helper(request)
    cur_month = date.replace('-', '')
    pre_month = get_previous_month(date)

    cursor = connection.cursor()
    cursor.execute("""
        select date, model, sum(sales) as sales, sum(num) as num, verified_sku.brand
        from summary_monthlystoreitemsummary
        join
            (select barcode, brand from standard_standarditem
             where standard_standarditem.status = 'human_verified' and
                (%s) and (%s)
            ) as verified_sku
        on verified_sku.barcode = summary_monthlystoreitemsummary.barcode
        where (%s) and (date = '%s' or date = '%s')
        group by brand, date, model;
    """ % (category_sql, vendor_sql, store_sql, pre_month, cur_month))
    all_sales = dictfetchall(cursor)

    cursor = connection.cursor()
    cursor.execute("""
        select date, model, sum(sales) as sales, sum(num) as num
        from summary_monthlystoreitemsummary
        join
            (select barcode from standard_standarditem
             where standard_standarditem.status = 'human_verified' and
                  (%s)
            ) as verified_sku
        on verified_sku.barcode = summary_monthlystoreitemsummary.barcode
        where (%s) and (date = '%s' or date = '%s') and model <> ''
        group by date, model;
        """ % (category_sql, store_sql, pre_month, cur_month))

    overall_sales = dictfetchall(cursor)
    result = sales_model_vendor_brand_helper(all_sales, overall_sales, cur_month, pre_month)

    if not store_name:
        cursor = connection.cursor()
        cursor.execute("""
            select count(distinct store_id) as total_store
            from summary_monthlystoreitemsummary
            join
                (select barcode, vendor from standard_standarditem
                 where standard_standarditem.status = 'human_verified' and
                      (%s)
                ) as verified_sku
            on verified_sku.barcode = summary_monthlystoreitemsummary.barcode
            where (date = '%s' or date = '%s');
        """ % (category_sql, pre_month, cur_month))
        total_store = dictfetchall(cursor)[0]['total_store']
    else:
        total_store = None

    cursor = connection.cursor()
    cursor.execute("""
        select sum(num_trades) as total from summary_monthlystoresummary
        where %s
    """ % store_sql)
    num_trades = int(dictfetchall(cursor)[0]['total'])

    return render(request, template, {'num_trades': num_trades, 'num_store': total_store, 'store_name': store_name, 'date': date, 'result': result, 'category': category_name})

@staff_member_required
def monthly_sales_vendor_model_flavor(request, date, template='summary/vendor_flavor.html'):
    vendor_sql, category_sql, store_sql, store_name, category_name = summary_params_helper(request)
    cur_month = date.replace('-', '')
    pre_month = get_previous_month(date)

    cursor = connection.cursor()
    cursor.execute("""
        select date, model, sum(sales) as sales, sum(num) as num, flavor, verified_sku.vendor
        from summary_monthlystoreitemsummary
        join
            (select barcode, vendor from standard_standarditem
             where standard_standarditem.status = 'human_verified' and
                (%s) and (%s)
            ) as verified_sku
        on verified_sku.barcode = summary_monthlystoreitemsummary.barcode
        where (%s) and (date = '%s' or date = '%s')
        group by flavor, date, model, verified_sku.vendor;
    """ % (category_sql, vendor_sql, store_sql, pre_month, cur_month))
    all_sales = dictfetchall(cursor)

    cursor = connection.cursor()
    cursor.execute("""
        select date, model, sum(sales) as sales, sum(num) as num, flavor
        from summary_monthlystoreitemsummary
        join
            (select barcode from standard_standarditem
             where standard_standarditem.status = 'human_verified' and
                  (%s)
            ) as verified_sku
        on verified_sku.barcode = summary_monthlystoreitemsummary.barcode
        where (%s) and (date = '%s' or date = '%s') and model <> '' and flavor <> ''
        group by flavor, date, model;
        """ % (category_sql, store_sql, pre_month, cur_month))

    overall_sales = dictfetchall(cursor)
    result = sales_model_vendor_model_flavor_helper(all_sales, overall_sales, cur_month, pre_month)
    if not store_name:
        cursor = connection.cursor()
        cursor.execute("""
            select count(distinct store_id) as total_store
            from summary_monthlystoreitemsummary
            join
                (select barcode, vendor from standard_standarditem
                 where standard_standarditem.status = 'human_verified' and
                      (%s)
                ) as verified_sku
            on verified_sku.barcode = summary_monthlystoreitemsummary.barcode
            where (date = '%s' or date = '%s');
        """ % (category_sql, pre_month, cur_month))
        total_store = dictfetchall(cursor)[0]['total_store']
    else:
        total_store = None

    cursor = connection.cursor()
    cursor.execute("""
        select sum(num_trades) as total from summary_monthlystoresummary
        where %s
    """ % store_sql)
    num_trades = int(dictfetchall(cursor)[0]['total'])

    return render(request, template, {'num_trades': num_trades, 'num_store': total_store, 'store_name': store_name, 'date': date, 'result': result, 'category': category_name})

################################################################################################
def init_day_template():
    # TODO: enable this when live and cronjob is running
    today = datetime.datetime.today()
    # today = datetime.date(2016, 6, 1)
    num_days = calendar.monthrange(today.year, today.month)[1]
    d = collections.OrderedDict()
    cur = datetime.date(today.year, today.month, 1)

    for i in range(num_days):
        d[str(cur)] = 0
        cur += datetime.timedelta(days=1)
    return d

def init_month_template():
    out = collections.OrderedDict()
    for i in range(1, 7):
        out['20160%d' % i] = 0
    return out

def item_sales_dict(sales, day_template):
    item_sales = {}
    for d in sales:
        if d['name'] not in item_sales:
            item_sales[d['name']] = collections.OrderedDict(day_template)
        date = str(d['date'])
        if date in day_template:
            item_sales[d['name']][date] += d['sales']

    out = {}
    for item, sales_dict in item_sales.items():
        out[item] = {'sales': sales_dict.values()}


    # growth
    for item, d in out.items():
        out[item]['growth'] = [0]
        sales = d['sales']
        for i in range(1, len(sales)):
            if sales[i - 1] == 0:
                growth = 0
            else:
                growth = round((sales[i] - sales[i - 1]) / sales[i - 1] * 100.0, 2)
                if growth > 0:
                    growth = '+%.2f' % growth

            out[item]['growth'].append(growth)

    return out


def store_item_sales_dict(sales, month_template):
    out = collections.OrderedDict(month_template)
    for d in out:
        out[d] = {}

    items = set()
    for row in sales:
        items.add(row['name'])

    for row in sales:
        m = str(row['date'])
        store_name = row['store_name']
        item_name = row['name']
        s = row['sales']
        if store_name not in out[m]:
            out[m][store_name] = collections.OrderedDict()
            for item in items:
                out[m][store_name][item] = {'sales': 0, 'growth': 0}

        out[m][store_name][item_name]['sales'] = s

    # compute growth
    months = month_template.keys()
    for m_idx in range(1, len(months)):
        for store in out[months[m_idx]]:
            for item in out[months[m_idx]][store]:
                if store not in out[months[m_idx]] or store not in out[months[m_idx-1]]:
                   cur_sales = 0
                   pre_sales = 0
                else:
                    cur_sales = out[months[m_idx]][store][item]['sales']
                    pre_sales = out[months[m_idx-1]][store][item]['sales']

                if pre_sales == 0:
                    growth = '-'
                else:
                    growth = round((cur_sales - pre_sales) / pre_sales * 100.0, 2)
                    if growth > 0:
                        growth = '+%.2f' % growth
                out[months[m_idx]][store][item]['growth'] = growth

    # order store by sales
    return out, items



def new_products(request, template='new-product/home.html'):
    # TODO: fetch barcodes by user

    barcodes = request.GET.getlist('barcodes', None)
    barcodes_sql = ' or '.join(["barcode = '%s'" % b for b in barcodes])
    if barcodes_sql:
        barcodes_final = barcodes_sql
    else:
        return render(request, template, {'error': u'Please input barcodes'})

    cursor = connection.cursor()

    # coverage
    cursor.execute("""
        select sum(num_trades) as total from summary_monthlystoresummary
        join (select distinct store_id from summary_monthlystoreitemsummary where (%s)
        ) as stores
        on stores.store_id = summary_monthlystoresummary.store_id;
        """ % (barcodes_final, ))
    coverage = int(dictfetchall(cursor)[0]['total'])

    # daily data
    cursor.execute("""
            select date, verified_sku.name, sum(sales) as sales, sum(num) as num
            from summary_dailystoreitemsummary
            join
                (select barcode, name, vendor from standard_standarditem
                 where standard_standarditem.status = 'human_verified' and
                      (%s)
                ) as verified_sku
            on verified_sku.barcode = summary_dailystoreitemsummary.barcode
            where date between '2016-07-01' and '2016-07-30'
            group by date, verified_sku.name;
        """ % (barcodes_final, ))

    day_template = init_day_template()
    daily_result = dictfetchall(cursor)
    daily = item_sales_dict(daily_result, day_template)

    # fetch previous months data
    cursor = connection.cursor()
    cursor.execute("""
            select date, store_store.name as store_name, verified_sku.name, sum(sales) as sales, sum(num) as num
            from summary_monthlystoreitemsummary
            join
                (select barcode, name, vendor from standard_standarditem
                 where standard_standarditem.status = 'human_verified' and
                      (%s)
                ) as verified_sku
            on verified_sku.barcode = summary_monthlystoreitemsummary.barcode
            join store_store
            on store_store.id = summary_monthlystoreitemsummary.store_id
            where date between '201601' and '201608'
            group by date, model, verified_sku.name, store_store.name;
        """ % (barcodes_final, ))

    month_template = init_month_template()
    monthly_sales = dictfetchall(cursor)

    monthly = item_sales_dict(monthly_sales, month_template)
    detail, sku = store_item_sales_dict(monthly_sales, month_template)

    return render(request, template, {'daily': json.dumps(daily), 'days': day_template.keys(), 'monthly': json.dumps(monthly), 'months': month_template.keys(), 'detail': json.dumps(detail), 'detail_data': detail, 'sku': sku, 'coverage': coverage})







@staff_member_required
def summary_detail(request, date, template='summary/table.html'):
    form = QueryForm(request.GET or None)
    filter_sql = '1=1'
    store_sql = '1=1'
    if form.is_valid():
        filter_sql = sql_utils.query_builder(form.cleaned_data['q'], {u'规格': 'model',
                                                                      u'口味': 'flavor',
                                                                      u'类别': 'category_id',
                                                                      u'供应商': 'vendor',
                                                                      u'品牌': 'brand'})

    cur_month = date.replace('-', '')
    pre_month = get_previous_month(date)

    cursor = connection.cursor()
    cursor.execute("""
        SELECT rank, rank_changed, item_name, sales, num, growth_rate, percentage, percentage_changed, model, flavor, category, vendor, brand
        from (
            -- compute rank_changed, percnetage_changed
            select
                 date,
                 item_name,
                 sales,
                 num,
                 model,
                 flavor,
                 category,
                 vendor,
                 brand,
                 growth_rate,
                 rank,
                 lag(rank) over(partition by item_name order by date asc) - rank as rank_changed,
                 percentage,
                 percentage - lag(percentage) over(partition by item_name order by date asc) as percentage_changed
            from(
                -- compute growth_rate, rank, percentage
                select *,
                       (sales -
                         lag(sales) over(partition by item_name order by date asc))
                       / lag(sales) over(partition by item_name order by date asc) * 100.0 as growth_rate,
                       rank() over(partition by date order by sales desc) as rank,
                       sales / sum(sales) over(partition by date) * 100.0 as percentage
                from (select
                            date,
                            verified_sku.barcode,
                            verified_sku.name as item_name,
                            verified_sku.model,
                            verified_sku.flavor,
                            standard_category.name as category,
                            verified_sku.vendor_txt as vendor,
                            verified_sku.brand,
                            sum(mss.sales) as sales,
                            sum(mss.num) as num
                    from summary_monthlystoreitemsummary mss
                    join
                        (select barcode, model, name, flavor, vendor_txt as vendor, vendor_short_name_txt as brand from standard_standarditem
                         where
                            standard_standarditem.status = 'human_verified'
                            and (%s)
                        ) as verified_sku
                        on verified_sku.barcode = mss.barcode
                    join store_storeitem on store_storeitem.id = mss.item_id
                    join standard_category on standard_category.id = mss.category_id
                    where (date='%s' or date='%s') and (%s)
                    group by date, verified_sku.barcode, verified_sku.name, verified_sku.model, verified_sku.flavor, standard_category.name, verified_sku.brand, verified_sku.vendor
                )agg_sales
            )sales_growth_rank
        )final
        where date='%s'
        order by rank;
        """ % (filter_sql, cur_month, pre_month, store_sql, cur_month))

    header = [u'排名', u'排名(+/-)', u'商品', u'销售额', u'销量', u'增長', u'佔比%', u'佔比(+/- pts)',  u'规格*', u'口味*', u'类别*', u'供应商*', u'品牌*']
    content = []
    for raw_row in cursor.fetchall():
        row = list(raw_row)
        if row[1] > 0:
            row[1] = '+%d' % row[1]

        if row[5]:
            if row[5] > 0:
                row[5] = '+%.2f' % round(row[5], 2)
            else:
                row[5] = round(row[5], 2)

        row[6] = round(row[6], 2)

        if row[7]:
            if row[7] > 0:
                row[7] = '+%.2f' % round(row[7], 2)
            else:
                row[7] = round(row[7], 2)

        content.append(row)

    return render(request, template, {'header': header, 'content': content, 'date': cur_month, 'form': form})


@staff_member_required
def summary_vendor_rank(request, date, template='summary/table.html'):
    form = QueryForm(request.GET or None)
    filter_sql = '1=1'
    if form.is_valid():
        filter_sql = sql_utils.query_builder(form.cleaned_data['q'], {u'类别': 'category_id',
                                                                      u'供应商': 'vendor'})
    print 'ha'
    print filter_sql
    cur_month = date.replace('-', '')
    pre_month = get_previous_month(date)

    cursor = connection.cursor()
    cursor.execute("""
        SELECT rank, rank_changed, vendor, sales, growth_rate, percentage, percentage_changed
        from (
            select *,
                percentage - lag(percentage) over(partition by vendor order by date asc) as percentage_changed
            from (
                select *,
                      sales / overall_sales * 100.0  as percentage,
                      lag(rank) over(partition by vendor order by date asc) - rank as rank_changed
                from (
                    select
                        mss.date,
                        sum(mss.sales) as sales,
                        overall.sales as overall_sales,
                       rank() over(partition by mss.date order by sum(mss.sales) desc) as rank,
                        verified_sku.vendor,
                       (sum(mss.sales) -
                         lag(sum(mss.sales)) over(partition by verified_sku.vendor order by mss.date asc))
                       / lag(sum(mss.sales)) over(partition by verified_sku.vendor order by mss.date asc) * 100.0 as growth_rate
                    from summary_monthlystoreitemsummary mss
                    join (
                        select barcode, vendor from standard_standarditem
                         where standard_standarditem.status = 'human_verified' and (%s)
                    ) as verified_sku
                    on verified_sku.barcode = mss.barcode
                    join (
                        -- overall sales
                        select
                            m.date,
                            sum(sales) as sales
                        from summary_monthlystoreitemsummary m
                        join (select barcode, vendor from standard_standarditem
                             where standard_standarditem.status = 'human_verified'
                            ) as verified_sku
                        on verified_sku.barcode = m.barcode
                        where (m.date='%s' or m.date='%s')
                        group by m.date
                    ) as overall
                    on overall.date = mss.date
                    where (mss.date='%s' or mss.date='%s')
                    group by vendor, mss.date, overall.sales
                )with_growth_rate
            )with_percentage
        )with_percentage_changed
        where date='%s'
        order by rank;
        """ % (filter_sql, cur_month, pre_month, cur_month, pre_month, cur_month))

    header = [u'排名', u'排名(+/-)', u'供应商*', u'销售额', u'增長%', u'份额%', u'份额(+/- pts)']
    content = []
    for raw_row in cursor.fetchall():
        row = list(raw_row)
        if row[1] > 0:
            row[1] = '+%d' % row[1]

        if row[4]:
            if row[4] > 0:
                row[4] = '+%.2f' % round(row[4], 2)
            else:
                row[4] = round(row[4], 2)

        row[5] = round(row[5], 2)

        if row[6]:
            if row[6] > 0:
                row[6] = '+%.2f' % round(row[6], 2)
            else:
                row[6] = round(row[6], 2)

        content.append(row)

    return render(request, template, {'header': header, 'content': content, 'date': cur_month, 'form': form})

def new_products(request, template='new-product/home.html'):
    # TODO: fetch barcodes by user

    barcodes = request.GET.getlist('barcodes', None)
    barcodes_sql = ' or '.join(["barcode = '%s'" % b for b in barcodes])
    if barcodes_sql:
        barcodes_final = barcodes_sql
    else:
        return render(request, template, {'error': u'Please input barcodes'})

    cursor = connection.cursor()

    # coverage
    cursor.execute("""
        select sum(num_trades) as total from summary_monthlystoresummary
        join (select distinct store_id from summary_monthlystoreitemsummary where (%s)
        ) as stores
        on stores.store_id = summary_monthlystoresummary.store_id;
        """ % (barcodes_final, ))
    coverage = int(dictfetchall(cursor)[0]['total'])

    # daily data
    sss = """
            SELECT date, verified_sku.name, sum(sales) as sales, sum(num) as num
            from summary_dailystoreitemsummary
            join
                (select barcode, name, vendor_short_name_txt from standard_standarditem
                 where standard_standarditem.status = 'human_verified' and
                      (%s)
                ) as verified_sku
            on verified_sku.barcode = summary_dailystoreitemsummary.barcode
            where date between '2016-06-01' and '2016-06-30'
            group by date, verified_sku.name;
        """ % (barcodes_final, )
    print sss
    cursor.execute(sss)

    day_template = init_day_template()
    daily_result = dictfetchall(cursor)
    daily = item_sales_dict(daily_result, day_template)

    # fetch previous months data
    cursor = connection.cursor()
    cursor.execute("""
            SELECT date, store_store.name as store_name, verified_sku.name, sum(sales) as sales, sum(num) as num
            from summary_monthlystoreitemsummary
            join
                (select barcode, name, vendor_short_name_txt from standard_standarditem
                 where standard_standarditem.status = 'human_verified' and
                      (%s)
                ) as verified_sku
            on verified_sku.barcode = summary_monthlystoreitemsummary.barcode
            join store_store
            on store_store.id = summary_monthlystoreitemsummary.store_id
            where date between '201601' and '201608'
            group by date, model, verified_sku.name, store_store.name;
        """ % (barcodes_final, ))

    month_template = init_month_template()
    monthly_sales = dictfetchall(cursor)

    monthly = item_sales_dict(monthly_sales, month_template)
    detail, sku = store_item_sales_dict(monthly_sales, month_template)

    return render(request, template, {'daily': json.dumps(daily), 'days': day_template.keys(), 'monthly': json.dumps(monthly), 'months': month_template.keys(), 'detail': json.dumps(detail), 'detail_data': detail, 'sku': sku, 'coverage': coverage})

@login_required(login_url='/login/')
def operational_analysis(request, date, template='operational-analysis/operational-analysis.html'):
    stores = Store.objects.filter(keeper=request.user)
    stores_daily_sales = DailyStoreItemSummary.objects.filter(store__in=stores).values('store_id').annotate(stores_daily_sales = Count('store_id')).order_by('stores_daily_sales')
    stores_daily_sales_volume = DailyStoreSummary.objects.filter(store__in=stores, date=date)
    # import random
    # store_items = StoreItem.objects.filter(store__in=stores)
    # [StoreItemInventory.objects.get_or_create(store_item=store_item, purchase_price=float("{0:.2f}".format(random.uniform(1, 4))), inventory=random.randint(50, 400)) for store_item in store_items]
    store_sales = DailyStoreItemSummary.objects.filter(store__in=stores, date=date).values('store_id').annotate(daily_sales = Sum('sales'), num=Sum('num'))
    for sales in store_sales:
        print sales
    stores_items_nums = StoreItem.objects.filter(store__in=stores).values('store_id').annotate(stores_items_num = Count('status'))
    for item in stores_items_nums:
        print item

    from django.db import connection
    with connection.cursor() as cursor:

        cursor.execute('''SELECT store_id, sum(purchase_price*num) AS cost_price, sum(sales) as sales from store_storeiteminventory join summary_dailystoreitemsummary on store_storeiteminventory.store_item_id=summary_dailystoreitemsummary.item_id where summary_dailystoreitemsummary.date=%s group by store_id''', [date])
        columns = [col[0] for col in cursor.description]
        cost_and_sales = [dict(zip(columns, row)) for row in cursor.fetchall()]
        for c in cost_and_sales:
            print c

    for volume in stores_daily_sales_volume:
        print volume.store.id, volume.num_sku, volume.num, volume.num_trades, volume.sales
    return render(request, template)





