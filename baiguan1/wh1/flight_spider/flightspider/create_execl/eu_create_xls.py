# -*- coding:utf-8 -*-
import xlwt
import zipfile
from flightspider import database
from datetime import timedelta, date


def init_execl():
    workbook = xlwt.Workbook(encoding='utf-8')
    res_sheet = workbook.add_sheet('euchange')
    dateFormat = xlwt.XFStyle()
    dateFormat.num_format_str = 'yyyy-mm-dd'
    res_sheet.write(0, 0, '航空公司')
    res_sheet.write(0, 1, '政策代码')
    res_sheet.write(0, 2, '起飞城市')
    res_sheet.write(0, 3, '到达城市')
    res_sheet.write(0, 4, '航班限制')
    res_sheet.write(0, 5, '航班号')
    res_sheet.write(0, 6, '班期限制')
    res_sheet.write(0, 7, '适用舱位')
    res_sheet.write(0, 8, '票面价类型')
    res_sheet.write(0, 9, '票面价/折扣')
    res_sheet.write(0, 10, 'CPA返点')
    res_sheet.write(0, 11, 'CPA留钱')
    res_sheet.write(0, 12, '销售起始日期')
    res_sheet.write(0, 13, '销售结束日期')
    res_sheet.write(0, 14, '旅行起始日期')
    res_sheet.write(0, 15, '旅行结束日期')
    res_sheet.write(0, 16, '航班起飞时间')
    res_sheet.write(0, 17, '最晚提前出票时限')
    res_sheet.write(0, 18, '最早提前出票时限')
    res_sheet.write(0, 19, '退改签说明')
    res_sheet.write(0, 20, '舱位说明')
    res_sheet.write(0, 21, '是否自动出票')
    res_sheet.write(0, 22, '搭桥office号')
    res_sheet.write(0, 23, '是否提供行程单')
    res_sheet.write(0, 24, 'CPA退票规则')
    res_sheet.write(0, 25, 'CPA改期规则')
    res_sheet.write(0, 26, 'CPA是否允许签转')
    res_sheet.write(0, 27, '是否提供常旅客积分')
    res_sheet.write(0, 28, '证件类型')
    res_sheet.write(0, 29, '预定office')
    res_sheet.write(0, 30, '是否支持代码共享航班')
    res_sheet.write(0, 31, '是否支持经停航班')
    res_sheet.write(0, 32, 'CPA投放类型')
    res_sheet.write(0, 33, 'CPA投放指定金额/下浮比例')
    res_sheet.write(0, 34, 'CPC返点')
    res_sheet.write(0, 35, 'CPC留钱')
    res_sheet.write(0, 36, 'CPC退票规则')
    res_sheet.write(0, 37, 'CPC改期规则')
    res_sheet.write(0, 38, 'CPC是否允许签转')
    res_sheet.write(0, 39, '出票速度')
    return res_sheet, dateFormat, workbook


def get_detail(res_sheet, workbook, dateFormat):
    tasks = database.get_detail_task()
    line_num = 1
    for task in tasks:
        company = task["flightNo"][:2]# 0
        dacode = task["daCode"]
        list_code = dacode.split('-')
        depcode = list_code[0]# 2
        arrcode = list_code[1]# 3
        flightno = task["flightNo"]# 5
        cabin = task["cabinId"]# 7
        price_type = '指定票面价'# 8
        price = task["price"]# 9
        cpa_point = 0# 10
        cpa_money = 20# 11
        sell_start = date.today()# 12
        eu_info = database.get_base_data(flightno, depcode, arrcode, 'EU')
        if eu_info is None:
            continue
        start_time = eu_info["planTime"].replace(":", "")# 16
        list_time = start_time.split('-')
        if list_time[0] > list_time[1]:
            travel_end_time = task["flightDate"] + timedelta(1) # 13 14 15
        else:
            travel_end_time = task["flightDate"]
        flight_change = database.get_cabin_change(cabin, 'EU')
        description = flight_change["description"]# 19
        auto_ticket = '否'# 21
        cpa_refund_rules = flight_change["refund_rules"]# 24
        cpa_change_rules = flight_change["change_rules"]# 25
        cpa_endorse = flight_change["change"]# 26
        integral = '否'# 27
        id_type = 1# 28
        share = '非共享'# 30
        mid_stop = '非经停'# 31
        cpa_type = '指定金额'# 32
        cpa_proportion = 5# 33
        cpc_point = 0# 34
        cpc_money = 20# 35
        flight_limit = '适用'
        week = task["flightDate"].weekday() + 1
        str_change = flight_change["change"]
        # cpc退票
        cpc_refund_rules = cpa_refund_rules
        # cpc改签
        cpc_change_rules = cpa_change_rules

        res_sheet.write(line_num, 0, company)
        res_sheet.write(line_num, 2, depcode)
        res_sheet.write(line_num, 3, arrcode)
        res_sheet.write(line_num, 4, flight_limit)
        res_sheet.write(line_num, 5, flightno)
        res_sheet.write(line_num, 6, week)
        res_sheet.write(line_num, 7, cabin)
        res_sheet.write(line_num, 8, price_type)
        res_sheet.write(line_num, 9, price)
        res_sheet.write(line_num, 10, cpa_point)
        res_sheet.write(line_num, 11, cpa_money)
        res_sheet.write(line_num, 12, sell_start, dateFormat)
        res_sheet.write(line_num, 13, travel_end_time, dateFormat)
        res_sheet.write(line_num, 14, travel_end_time, dateFormat)
        res_sheet.write(line_num, 15, travel_end_time, dateFormat)
        res_sheet.write(line_num, 16, '0000-2359')
        res_sheet.write(line_num, 17, 0)
        res_sheet.write(line_num, 18, 0)
        res_sheet.write(line_num, 19, description)
        res_sheet.write(line_num, 20, '对比采购渠道，以价格最优方式出票')
        res_sheet.write(line_num, 21, auto_ticket)
        res_sheet.write(line_num, 23, 1)
        res_sheet.write(line_num, 24, cpa_refund_rules)
        res_sheet.write(line_num, 25, cpa_change_rules)
        res_sheet.write(line_num, 26, cpa_endorse)
        res_sheet.write(line_num, 27, integral)
        res_sheet.write(line_num, 28, id_type)
        # 29 预定office,可为空
        res_sheet.write(line_num, 29, 'PEK302')
        res_sheet.write(line_num, 30, share)
        res_sheet.write(line_num, 31, mid_stop)
        res_sheet.write(line_num, 32, cpa_type)
        res_sheet.write(line_num, 33, cpa_proportion)
        res_sheet.write(line_num, 34, cpc_point)
        res_sheet.write(line_num, 35, cpc_money)
        res_sheet.write(line_num, 36, cpc_refund_rules)
        res_sheet.write(line_num, 37, cpc_change_rules)
        res_sheet.write(line_num, 38, str_change)
        res_sheet.write(line_num, 39, 30)
        line_num += 1
    workbook.save(r'/home/kyfw/worker/flightspider/flightspider/download/static/eu_change.xls')


def create_zipfile():
    z = zipfile.ZipFile(r'/home/kyfw/worker/flightspider/flightspider/download/static/eu_change.zip', mode='w', compression=zipfile.zlib.DEFLATED)
    z.write(r'/home/kyfw/worker/flightspider/flightspider/download/static/eu_change.xls', './eu_change.xls')


def eu_xls():
    res_sheet, dateFormat, workbook = init_execl()
    get_detail(res_sheet, workbook, dateFormat)
    create_zipfile()


def main():
    eu_xls()


if __name__ == '__main__':
    main()
