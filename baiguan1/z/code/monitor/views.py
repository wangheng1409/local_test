# -*- coding: utf-8 -*-

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.conf import settings
from django.db import connection
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage

from operator import itemgetter
import re
import collections
import datetime
import calendar
import json
from .models import MonitorBarcodes

from core import choices, sql_utils
from collections import defaultdict
import pandas

from .forms import DateRangePickerForm
from synclog.models import SpiderSyncLog 


def get_previous_month(date_str, splitter=''):
    tok = date_str.split('-')
    int_month = int(tok[1])
    if int_month == 1:
        return '%d%s12' % (int(tok[0]) - 1, splitter)
    else:
        int_month -= 1
        if int_month < 10:
            return '%s%s0%d' % (tok[0], splitter, int_month)
        return '%s%s%d' % (tok[0], splitter, int_month)


def get_next_month(date_str, splitter=''):
    tok = date_str.split('-')
    int_month = int(tok[1])
    if int_month == 12:
        return '%d%s01' % (int(tok[0]) + 1, splitter)
    else:
        int_month += 1
        if int_month < 10:
            return '%s%s0%d' % (tok[0], splitter, int_month)
        return '%s%s%d' % (tok[0], splitter, int_month)


def key_value_map(cur):
    out = {}
    for c in cur.fetchall():
        out[c[0]] = c[1]
    return out


def nested_dd():
    return defaultdict(nested_dd)


def store_item_values(cur, store_names_map, item_names_map):
    # store -> many items -> values
    out = nested_dd()
    r = sql_utils.dictfetchall(cur)
    for c in r:
        store_name = store_names_map[c['store_id']]
        item_name = item_names_map[c['barcode']]
        out[store_name]['id'] = c['store_id']
        out[store_name]['p'][item_name]['barcode'] = c['barcode']
        out[store_name]['p'][item_name]['sales'] = c['sales']
        out[store_name]['p'][item_name]['num'] = c['num']
        out[store_name]['p'][item_name][
            'growth'] = sql_utils.growth_rate(c['growth'])

    out.default_factory = None
    for store, values in out.items():
        values.default_factory = None
        values['p'].default_factory = None
        for item, v in values['p'].items():
            v.default_factory = None
    return out


def last_day_of_month(date):
    if date.month == 12:
        return date.replace(day=31)
    return date.replace(month=date.month + 1, day=1) - datetime.timedelta(days=1)


def empty_home(request):
    return HttpResponse('Hi 超盟!')


@login_required(login_url='/login/')
def new_products_home(request):
    return redirect(reverse('new-products-monitoring', kwargs={'date': datetime.date.today().strftime('%Y-%m')}))


@login_required(login_url='/login/')
def new_products_v2(request, date, template='new-product/home2.html'):
    project_id = request.GET.get('p')
    if not project_id:
        if request.user.monitor_barcodes.exists():
            project = request.user.monitor_barcodes.last()
        else:
            return HttpResponse(u'请先开通服务')
    else:
        try:
            project = request.user.monitor_barcodes.get(
                pk=project_id, user=request.user)
        except MonitorBarcodes.DoesNotExist:
            raise Http404(u'项目不存在')

    # monthly sales: store vs items
    pre_month = get_previous_month(date)
    cur_month = date.replace('-', '')

    first_day = '%s-01' % date
    last_day = '%s-%d' % (date, last_day_of_month(
        datetime.datetime.strptime(date, '%Y-%m').date()).day)

    my_projects = request.user.monitor_barcodes.order_by(
        '-created_at').values('id', 'name')

    barcodes_src = list(project.barcodes.values_list('barcode', flat=True))
    barcodes_values = ','.join(["('%s')" % b for b in barcodes_src])

    barcodes = ' or '.join(["barcode='%s'" % b for b in barcodes_src])
    dates = "date=%s or date=%s" % (pre_month, cur_month)

    cur = connection.cursor()
    # store_id -> store_name
    cur.execute("""
        SELECT
            ids.store_id,
            store_store.name
        from store_store
        join
        (select distinct store_id from summary_monthlystoreitemsummary where (%s) and (%s))ids
        on ids.store_id = store_store.store_id;
    """ % (barcodes, dates))
    store_names_map = key_value_map(cur)

    # barcode -> item
    cur.execute("""
        SELECT barcode, name from standard_standarditem ssi where (%s)
    """ % barcodes)
    item_names_map = key_value_map(cur)

    # store_id, barcode, sales, num, growth
    cur.execute("""
        SELECT store_id, barcode, sales, num, growth
            from (
            select
                idx.date,
                idx.store_id,
                idx.barcode,
                coalesce(src.sales, 0) as sales,
                coalesce(src.num, 0) as num,
                CASE lag(src.sales) over (partition by idx.barcode, idx.store_id order by idx.date asc)
                    WHEN 0 THEN NULL
                ELSE
                    (coalesce(src.sales, 0) - lag(coalesce(src.sales, 0)) over (partition by idx.barcode, idx.store_id order by idx.date asc))
                    / lag(src.sales) over (partition by idx.barcode, idx.store_id order by idx.date asc) * 100.0
                END as growth
            from
                (select * from
                    (select * from (values (%(pre_month)s), (%(cur_month)s)) as dates(date))a
                    cross join
                        (select * from
                            (select distinct store_id from summary_monthlystoreitemsummary
                             where (%(barcodes)s) and (%(dates)s)
                         )store_ids
                    cross join
                    (select barcodes.barcode from (values %(barcode_values)s) as barcodes(barcode))barcode)store_x_barcode
                )idx
            left join
                (select
                    date,
                    store_id,
                    barcode,
                    sum(sales) as sales,
                    sum(num) as num
                 from summary_monthlystoreitemsummary
                 where (%(barcodes)s) and (%(dates)s)
                 group by date, barcode, store_id)src
            on idx.date = src.date and idx.store_id = src.store_id and idx.barcode=src.barcode)final
        where final.date=%(cur_month)s;
    """ % {'pre_month': pre_month, 'cur_month': cur_month, 'barcodes': barcodes, 'dates': dates, 'barcode_values': barcodes_values})

    stores_table = store_item_values(cur, store_names_map, item_names_map)
    sql = """
        SELECT
            barcode,
            array_agg(sales order by date asc) as sales,
            array_agg(num order by date asc) as nums,
            array_agg(growth order by date asc) as growth
        from(
            select
                idx.date,
                idx.barcode,
                coalesce(src.sales, 0) as sales,
                coalesce(src.num, 0) as num,
                coalesce((coalesce(src.sales, 0) - lag(coalesce(src.sales, 0)) over (partition by idx.barcode order by idx.date asc))
                 / lag(src.sales) over (partition by idx.barcode order by idx.date asc) * 100.0, 0) as growth
            from
                (select
                        *
                        from (select generate_series('%(first_day)s', '%(last_day)s', '1 day'::interval)::date as date)days
                        cross join
                        (select * from (values %(barcode_values)s) as barcodes(barcode))barcodes
                )idx
            left join(
                SELECT
                    date,
                    barcode,
                    sum(sales) as sales,
                    sum(num) as num
                from summary_dailystoreitemsummary
                where (%(barcodes)s) and (date >= '%(first_day)s' and date <= '%(last_day)s')
                group by date, barcode)src
            on idx.date = src.date and idx.barcode = src.barcode)out
        group by barcode;
    """ % {'first_day': first_day, 'last_day': last_day, 'barcode_values': barcodes_values, 'barcodes': barcodes}
    cur.execute(sql)
    daily = sql_utils.dictfetchall(cur)
    for i in range(len(daily)):
        daily[i]['item_name'] = item_names_map[daily[i]['barcode']]
        daily[i]['growth'] = ['%.2f' % round(v, 2) for v in daily[i]['growth']]
        daily[i]['sales'] = ['%.2f' % round(v, 2) for v in daily[i]['sales']]

    l = pandas.date_range(first_day, last_day)
    x_axis = []
    for i in l:
        x_axis.append('%02d-%02d %s' %
                      (i.month, i.day, i.weekday_name[:3].upper()))

    ######
    # date, tag, barcode, sales, num, growth
    ######
    cur.execute("""
        select id, name from store_storetag;
    """)
    tag_names_map = key_value_map(cur)
    sql = """
        SELECT
            tag_id,
            array_agg(sales order by barcode) as sales,
            array_agg(num order by barcode) as num,
            array_agg(growth order by barcode) as growth,
            array_agg(barcode order by barcode) as barcodes
        FROM (
            SELECT
                idx.date,
                idx.tag_id,
                idx.barcode,
                coalesce(src.sales, 0) as sales,
                coalesce(src.num, 0) as num,
                coalesce((coalesce(src.sales, 0) - lag(coalesce(src.sales, 0)) over (partition by idx.barcode, idx.tag_id order by idx.date asc))
                 / lag(src.sales) over (partition by idx.barcode, idx.tag_id order by idx.date asc) * 100.0, 0) as growth
            from (select * from
                    (select * from (values (%(pre_month)s), (%(cur_month)s)) as dates(date))a
                    cross join
                        (select * from
                                (
                                    SELECT
                                        distinct unnest(ss.tags) as tag_id
                                    from (
                                        SELECT
                                            distinct store_id
                                        from summary_monthlystoreitemsummary
                                        where (%(barcodes)s) and (%(dates)s)
                                    )stores
                                    join store_store ss
                                    on ss.store_id = stores.store_id
                                )tags
                                cross join
                                (select barcodes.barcode from (values %(barcode_values)s) as barcodes(barcode))barcode
                        )tag_x_barcode
                    )idx
                left join (
                    select
                        date,
                        unnest(ss.tags) as tag_id,
                        barcode,
                        sum(sales) as sales,
                        sum(num) as num
                    from summary_monthlystoreitemsummary summary
                    join store_store ss
                    on ss.store_id = summary.store_id
                    where (%(barcodes)s) and (%(dates)s)
                    group by date, barcode, tag_id)src
                on idx.date = src.date and idx.tag_id = src.tag_id and idx.barcode = src.barcode)final
        where final.date=%(cur_month)s
        group by tag_id;
        """ % {'pre_month': pre_month, 'cur_month': cur_month, 'barcodes': barcodes, 'dates': dates, 'barcode_values': barcodes_values}
    cur.execute(sql)
    tags = sql_utils.dictfetchall(cur)
    for i in range(len(tags)):
        tags[i]['item_name'] = tag_names_map[tags[i]['tag_id']]
        tags[i]['growth'] = ['%.2f' % round(v, 2) for v in tags[i]['growth']]
        tags[i]['sales'] = ['%.2f' % round(v, 2) for v in tags[i]['sales']]
        tags[i]['item_names'] = [item_names_map[v]
                                 for v in tags[i]['barcodes']]

    return render(request, template, {'cur_month': date,
                                      'pre_month': get_previous_month(date, splitter='-'),
                                      'next_month': get_next_month(date, splitter='-'),
                                      'cur_project': project,
                                      'my_projects': my_projects,
                                      'stores_table': stores_table,
                                      'items': item_names_map.values(),
                                      'x_axis': x_axis,
                                      'daily': json.dumps(daily),
                                      'tags': json.dumps(tags)})


@staff_member_required
def monitor_brand_items(request, template='monitor/monitor_brand_items.html'):

    form = DateRangePickerForm(request.GET or None)
    if not form.is_valid():
        return HttpResponse('missing brand')

    start_date = form.cleaned_data.get('start_date')
    if not start_date:
        start_date = (datetime.date.today() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
    end_date = form.cleaned_data.get('end_date')
    if not end_date:
        end_date = datetime.date.today().strftime('%Y-%m-%d')
    brand = form.cleaned_data['brand']

    sql = """
    SELECT
        out.name,
        array_agg(out.sales) AS chart_data
    FROM (
        SELECT
            idx.date,
            idx.name,
            COALESCE(src.sales, 0) AS sales
        FROM (
            SELECT
                *
            FROM (
                SELECT generate_series('%(start_date)s', '%(end_date)s', '1 day'::interval)::date AS date
            ) days
            CROSS JOIN (
                SELECT
                    distinct name
                FROM standard_standarditem
                WHERE vendor_short_name_txt = '%(brand)s'
            ) names
        )idx
        LEFT JOIN (
            SELECT
                date,
                standards.name,
                sum(sales) AS sales
            FROM summary_dailystoreitemsummary summary
            JOIN (
                SELECT
                    barcode,
                    name
                FROM
                    standard_standarditem
                WHERE
                    vendor_short_name_txt = '%(brand)s'
            ) standards
            ON summary.barcode = standards.barcode
            GROUP BY date, standards.name
        )src
        ON idx.date = src.date AND idx.name = src.name
    ) out
    WHERE name IS NOT NULL
    GROUP BY out.name
    ORDER BY out.name;
    """ % {'start_date': start_date, 'end_date': end_date, 'brand': brand}

    cur = connection.cursor()
    cur.execute(sql)
    result = sql_utils.dictfetchall(cur)

    x_values = cur.execute("""
        SELECT array_agg(date) AS dates FROM (
            SELECT generate_series('%(start_date)s', '%(end_date)s', '1 day'::interval)::date AS date
        )out;
    """ % {'start_date': start_date, 'end_date': end_date})
    x_values = sql_utils.dictfetchall(cur)[0]['dates']

    return render(request, template, {'result': result,
                                      'x_values': x_values,
                                      'brand': brand,
                                      'start_date': start_date,
                                      'end_date': end_date
                                      })

def ads(request):
    return HttpResponse('hello');

@staff_member_required
def monitor_spider(request, template='monitor/monitor_spider.html'):
    page_num = request.GET.get('page_num')
    query_tag = request.GET.get('query_tag')
 
    x_values = []
    for dates_range in range(0,30): 
        last_date = (datetime.date.today() - datetime.timedelta(days=dates_range)).strftime('%m-%d')
        x_values = [last_date] + x_values 

    if query_tag in(None, 'None'):
        datas = SpiderSyncLog.objects.all()
    else:
        datas = SpiderSyncLog.objects.filter(Q(tag__icontains=query_tag))

    datas_dict = {}
    for data in datas:
        area = data.area
        source = data.source + '_' + area
        crawl_date = data.crawl_date.strftime('%m-%d')
        count = data.count
        tag = data.tag
        if tag not in datas_dict:
            datas_dict[tag] =  {}
        if source  not in datas_dict[tag]:    
            datas_dict[tag][source] = {}
        datas_dict[tag][source][crawl_date] = count

    results = []
    for tag,source_detail in datas_dict.items():
        result = {'tag':tag, 'data':{}}
        for source, date_detail in source_detail.items():
            result['data'][source] = []
            for x_date in x_values:
                count = date_detail.get(x_date, 0)
                result['data'][source].append(count)
        results.append(result)
    results.sort(key = lambda x: sum(x['data'].get('tmall_HD',[])),reverse = True)

    one_page_num = 100
    paginator = Paginator(results, one_page_num)
    try:
        results = paginator.page(page_num)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    return render(request, template, {'results': results,
                                      'x_values': x_values,
                                      'page_num': page_num,
                                      'query_tag': query_tag
                                      })
