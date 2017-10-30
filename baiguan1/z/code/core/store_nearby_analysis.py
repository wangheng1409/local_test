# -*- coding: utf-8 -*-
from django.db import connection
from core import sql_utils
from distance_bd import distance_bd

def get_store_nearby(distance,store_id):
    
    #item_geo
    sql = """
    select lat,lng from store_store where store_id ='%(store_id)s' 
    """ % {'store_id': store_id}
    cur = connection.cursor()
    cur.execute(sql)
    results = sql_utils.dictfetchall(cur)
    input_geo = {}
    if len(results) == 1:
        input_geo = results[0]

    #near_by items
    sql = """
    select store_id,lat,lng from store_store 
    where lat between '%(lat_min)s' and '%(lat_max)s' 
    and lng between '%(lng_min)s' and '%(lng_max)s' 
    """ % {'lat_min': input_geo['lat']-1, 'lat_max': input_geo['lat']+1, 'lng_min':input_geo['lng']-1, 'lng_max':input_geo['lng']+1}
    cur = connection.cursor()
    cur.execute(sql)
    results = sql_utils.dictfetchall(cur)
    items = []
    for item in results:
        item_geo = {'lat':item['lat'],'lng':item['lng']}
        dis = distance_bd(input_geo,item_geo) 
        if dis < distance:
            item['dis'] = dis
            items.append(item) 
    return items

def get_store_sales_category(store_id,start_date,end_date):

    sql = """
    select sum(sales) as sum_sales,category  
    from summary_dailystoreitemsummary
    where store_id = '%(store_id)s' and category is not null
    and date between to_date('%(start_date)s','YYYY-MM-DD') and to_date('%(end_date)s','YYYY-MM-DD') 
    group by category
    """ % {'start_date': start_date, 'end_date': end_date, 'store_id': store_id}
    cur = connection.cursor()
    cur.execute(sql)
    results = sql_utils.dictfetchall(cur)
    return results
