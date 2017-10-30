import pymongo
from datetime import timedelta, date
from collections import defaultdict
import json

client = pymongo.MongoClient('mongodb://root:Baiguan2016@60.205.152.167:3717')
db1 = client.monitor.detail

from flask import render_template
from flask import request

from flask import Flask

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def search():
    print('访问ip：',request.remote_addr)
    source = request.args.get('source', 'sj')
    start_day = request.args.get('start_day', str(date.today() - timedelta(days=7)))
    year,month,day=start_day.split(',')
    start_day='-'.join([year,month if len(month)==2 else '0'+month,day if len(day)==2 else '0'+day])
    if start_day=='2017-01-01':
        start_day=str(date.today() - timedelta(days=7))
    city = request.args.get('city', '全部')
    print(source,start_day)

    col = db1.find({'source': source, 'ts_string': {'$gte': start_day}}, {'ts_string': 1, 'data': 1, '_id': 0})
    col = [x for x in col]
    print(len(col))
    for i in range(len(col)):
        col[i]['data'] = col[i]['data'].get(city, 0)
    data={}
    data['X_axis']=[x['ts_string'] for x in col]
    data['Y_axis']=[x['data'] for x in col]
    print(data)

    return json.dumps(data)

@app.route('/city')
def city():
    source = request.args.get('source', 'sj')
    if source in ['sj', 'ky']:
        city_list = ['全部', '北京市', '沈阳市', '石家庄市', '太原市', '济南市', '开封市', '南京市', '合肥市', '南通市', '上海市', '成都市', '杭州市',
                     '金华市', '南昌市', '长沙市', '福州市', '泉州市', '广州市', '惠州市', '深圳市', '宜昌市',
                     ]
    else:
        city_list = ['全部', '鞍山', '安阳', '北京', '保定', '重庆', '成都', '长沙', '长春', '沧州', '大连', '福州', '佛山', '广州', '贵阳', '哈尔滨',
                     '杭州','合肥', '呼和浩特', '黄石', '邯郸', '济南', '吉林', '昆明', '兰州', '洛阳', '南京', '南昌', '南宁', '宁波', '南通', '南阳',
                     '青岛','秦皇岛', '上海', '沈阳', '深圳', '石家庄', '苏州', '十堰', '天津', '太原', '唐山', '武汉', '无锡', '乌鲁木齐', '温州',
                     '潍坊','西安', '厦门', '徐州', '襄阳', '湘潭', '宜昌', '烟台', '扬州', '永川', '郑州', '镇江', '株洲', '珠海', ]
    return json.dumps(city_list)


if __name__ == "__main__":
    # app.run(host='60.205.152.167', debug=True,port=8884)
    # app.run(host='192.168.22.198', debug=True,port=8884)
    app.run(host='127.0.0.1', debug=True,port=8884)
