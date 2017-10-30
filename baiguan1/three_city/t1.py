import pandas as pd
import json
import pymongo
import requests
from lxml import html
from lxml import etree
import time
import datetime


def table_json(url,xp):
    res=requests.get(url=url)
    # print(res.text)
    response=html.fromstring(res.text)
    try:
        table=response.xpath(xp)[0]
    except:
        raise Exception('XPATH ERROR')
    table=etree.tostring(table)
    # print(table)
    data =pd.read_html(table,encoding='utf8',)[0]
    # print(data,type(data))
    js = data.to_json(orient='index', force_ascii=False)

    return js

if __name__ == '__main__':
    city_dict={
        '镇江市':{'url':'http://221.6.146.72:9080/estate2/olestate/index.action',
                'xp':'//table[@height=80]',
                },
        '湖州市': {'url': 'http://www.hufdc.com/',
                'xp': '//dd[@id="myCont5"]/div[1]/table[@class="tabhzljcj"]',
                },
        '遵义市': {'url': 'http://www.gzzyfc.com.cn/Client/ZunYi/Second/Second_TodayTrade.aspx?type=trade&houseType=0&dateType=month&rnd=0.29356231116860654',
                'xp': '//table',
                },
        '锦州市': {'url': 'http://www.jzfc.com/pageservice/DayDeal.aspx',
                'xp': '//form/table/tr[2]/td/table',
                },
    }

    for k,v in city_dict.items():
        ret = table_json(v['url'], v['xp'])
        print(ret)
        client = pymongo.MongoClient('mongodb://root:Baiguan2016@60.205.152.167:3717')
        db = client.realestate
        s={'city':k,
           'detail':ret,
           'ts':datetime.datetime.fromtimestamp(time.time(), None),
           'ts_string':str(datetime.date.today()),
           }
        db.city_detail.insert(s)

