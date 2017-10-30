# -*- coding: utf-8 -*-
import datetime
from django.db import connection
from core import sql_utils

def loss_analysis(start_date,end_date,item_id):
    lose_days = 0
    lose_count = 0.0
    lose_dates = []
    maxPer = 0.5
    maxPerSecond = 0.001
    maxAve = 0.0
    loseThresholdPer = 0.7

    #search_data
    sql = """
    SELECT
      nq.sales,nq.name,nq.num,to_char(dates.date,'YYYY-MM-DD') as date 
    FROM
    (
     (SELECT
        sd.sales,ss.name,sd.date,sd.num 
      FROM 
        summary_dailystoreitemsummary as sd, store_storeitem as ss 
      WHERE 
        sd.date BETWEEN to_date('%(start_date)s','YYYY-MM-DD') AND to_date('%(end_date)s','YYYY-MM-DD') AND 
        sd.item_id = ss.id AND
        sd.item_id = '%(item_id)s') as nq 
      RIGHT JOIN
       (SELECT
          generate_series('%(start_date)s', '%(end_date)s', '1 day'::interval)::date AS date) dates 
      ON dates.date = nq.date
    )
    ORDER BY date 
    """ % {'start_date': start_date, 'end_date': end_date, 'item_id': item_id}

    cur = connection.cursor()
    cur.execute(sql)
    result = sql_utils.dictfetchall(cur)

    #his_data 
    his_start_date = (datetime.date.today() - datetime.timedelta(days=70)).strftime('%Y-%m-%d')
    his_end_date = datetime.date.today().strftime('%Y-%m-%d')
    sql = """
    SELECT
      nq.sales,nq.name,nq.num,to_char(dates.date,'YYYY-MM-DD') as date
    FROM
    (
     (SELECT
        sd.sales,ss.name,sd.date,sd.num 
      FROM summary_dailystoreitemsummary as sd, store_storeitem as ss 
      WHERE 
        sd.date BETWEEN to_date('%(start_date)s','YYYY-MM-DD') AND to_date('%(end_date)s','YYYY-MM-DD') AND
        sd.item_id = ss.id AND
        sd.item_id = '%(item_id)s') as nq 
    RIGHT JOIN 
     (SELECT
        generate_series('%(start_date)s', '%(end_date)s', '1 day'::interval)::date AS date
     ) dates 
    ON dates.date = nq.date
    )
    ORDER BY date 
    """ % {'start_date': his_start_date, 'end_date': his_end_date, 'item_id': item_id}

    cur = connection.cursor()
    cur.execute(sql)
    his_result = sql_utils.dictfetchall(cur)
    his_aves = [{'avg':0,'data':[]},{'avg':0,'data':[]},{'avg':0,'data':[]},{'avg':0,'data':[]},{'avg':0,'data':[]},{'avg':0,'data':[]},{'avg':0,'data':[]},]
    for r in his_result:
        myDate = r['date']
        sales = r['sales']
        if not sales:
            continue
        week = datetime.datetime.strptime(myDate, "%Y-%m-%d").weekday()
        his_aves[week]['data'].append(sales)
    for his_ave in his_aves:
        his_median = 0
        loseThreshold = 0
        if not his_ave['data']:
            his_ave['median'] = his_median
            his_ave['loseThreshold'] = loseThreshold
            continue
        his_median = median(his_ave['data'])
        loseThreshold = his_median * loseThresholdPer
        his_ave['median'] = his_median
        his_ave['loseThreshold'] = loseThreshold

    medians = []    
    for week in range(7):
        medians.append(his_aves[week].get('median',0))     
        
    #损失
    for r in result:
        sales = r['sales']
        if not sales:
            sales = 0
        myDate = r['date']
        week = datetime.datetime.strptime(myDate, "%Y-%m-%d").weekday()
        
        if sales < his_aves[week]['loseThreshold']:
            lose_dates.append(myDate)
            lose_count = lose_count+his_aves[week]['median']-sales
    lose_count = round(lose_count,5)
    lose_days=len(lose_dates)

    return {'lose_days':lose_days,'lose_dates':lose_dates,'lose_count':lose_count,'result':result,'medians':medians}
    

def median(lst):
    if not lst:
        return 
    lst=sorted(lst)
    if len(lst)%2==1:
        return lst[len(lst)//2]
    else:
        return  (lst[len(lst)//2-1]+lst[len(lst)//2])/2.0
