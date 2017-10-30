# -*- coding:utf-8 -*-
import xlwt
import zipfile
from flightspider import database
from datetime import timedelta, date


def pre_sheet(res_sheet):
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
    #res_sheet.write(0, 21, '是否自动出票')

    res_sheet.write(0, 21, '是否允许直接支付')
    res_sheet.write(0, 22, '是否生成PNR')
    res_sheet.write(0, 23, '进行PAT:A校验')

    res_sheet.write(0, 24, '搭桥office号')
    res_sheet.write(0, 25, '是否提供行程单')
    res_sheet.write(0, 26, 'CPA退票规则')
    res_sheet.write(0, 27, 'CPA改期规则')
    res_sheet.write(0, 28, 'CPA是否允许签转')
    res_sheet.write(0, 29, '是否提供常旅客积分')
    res_sheet.write(0, 30, '证件类型')

    res_sheet.write(0, 31, '最大购买年龄')
    res_sheet.write(0, 32, '最小购买年龄')
    res_sheet.write(0, 33, '特殊票务说明')

    res_sheet.write(0, 34, '预定office')
    res_sheet.write(0, 35, '是否支持代码共享航班')
    res_sheet.write(0, 36, '是否支持经停航班')
    res_sheet.write(0, 37, 'CPA投放类型')
    res_sheet.write(0, 38, 'CPA投放指定金额/下浮比例')
    res_sheet.write(0, 39, 'CPC返点')
    res_sheet.write(0, 40, 'CPC留钱')
    res_sheet.write(0, 41, 'CPC退票规则')
    res_sheet.write(0, 42, 'CPC改期规则')
    res_sheet.write(0, 43, 'CPC是否允许签转')

    res_sheet.write(0, 44, 'CPA报价类型')

    res_sheet.write(0, 45, '出票速度')


def init_execl(company):
    workbook = xlwt.Workbook(encoding='utf-8')
    res_sheet = workbook.add_sheet('%sprepay' % company.lower())
    dateFormat = xlwt.XFStyle()
    dateFormat.num_format_str = 'yyyy-mm-dd'
    pre_sheet(res_sheet)
    return res_sheet, dateFormat, workbook


def get_detail(company, res_sheet, workbook, dateFormat):
    tasks = database.get_detail_task(company)
    line_num = 1
    sheet_num = 0
    if len(tasks) == 0:
        return
    for task in tasks:
        #if company == 'JR' and task["surplusTicket"].isdigit():
        #    if int(task["surplusTicket"]) <= 5:
        #        continue
        #dacode = task["daCode"]
        #list_code = dacode.split('-')
        depcode = task["depCode"]
        arrcode = task["arrCode"]
        week = task["flightDate"].weekday() + 1
        sell_start = date.today()
        # 不同公司的差异处理
        eu_info = None
        if company == 'G5':
            try:
                eu_info = database.get_base_data(task["flightNo"], depcode, arrcode, company, week)
            except:
                print task["flightNo"], depcode, arrcode, company, week
                continue
        #elif company == 'EU':
        #    eu_info = database.get_base_data(task["flightNo"], depcode, arrcode, company)
        if eu_info is None and (company == "G5"):
            continue
        flight_change = database.get_cabin_change(task["cabinId"], company)
        if flight_change is None:
            continue
        # cpa退票规则24
        cpa_refund_rules = flight_change["refund_rules"]
        # cpa改签规则25
        cpa_change_rules = flight_change["change_rules"]
        # cpa签转26
        cpa_endorse = flight_change["change"]
        # cpa签转
        str_change = cpa_endorse
        # cpc退票
        cpc_refund_rules = cpa_refund_rules
        # cpc改签
        cpc_change_rules = cpa_change_rules
        # cpa投放类型
        cpa_type = '指定金额'
        # cpa投放指定金额
        cpa_proportion = 5

        res_sheet.write(line_num, 0, company)
        res_sheet.write(line_num, 2, depcode)
        res_sheet.write(line_num, 3, arrcode)
        res_sheet.write(line_num, 4, '适用')
        res_sheet.write(line_num, 5, task["flightNo"])
        res_sheet.write(line_num, 6, week)
        res_sheet.write(line_num, 7, task["cabinId"])
        res_sheet.write(line_num, 8, '指定票面价')
        res_sheet.write(line_num, 9, task["price"])
        # cpa返点、留钱
        res_sheet.write(line_num, 10, 0)
        res_sheet.write(line_num, 11, 20)
        res_sheet.write(line_num, 12, sell_start, dateFormat)
        res_sheet.write(line_num, 13, task["flightDate"], dateFormat)
        res_sheet.write(line_num, 14, task["flightDate"], dateFormat)
        res_sheet.write(line_num, 15, task["flightDate"], dateFormat)
        res_sheet.write(line_num, 16, '0000-2359')
        res_sheet.write(line_num, 17, 0)
        res_sheet.write(line_num, 18, 0)
        # 描述
        res_sheet.write(line_num, 19, flight_change["description"])
        res_sheet.write(line_num, 20, '对比采购渠道，以价格最优方式出票')
        # 是否自动出票
        #res_sheet.write(line_num, 21, '否')

        res_sheet.write(line_num, 21, '是')
        res_sheet.write(line_num, 22, '是')
        res_sheet.write(line_num, 23, '是')

        res_sheet.write(line_num, 25, 1)
        res_sheet.write(line_num, 26, cpa_refund_rules)
        res_sheet.write(line_num, 27, cpa_change_rules)
        res_sheet.write(line_num, 28, cpa_endorse)
        # 是否提供常旅客积分
        res_sheet.write(line_num, 29, '否')
        # 证件类型
        res_sheet.write(line_num, 30, 1)

        # res_sheet.write(0, 32, '')
        # res_sheet.write(0, 33, '')
        # res_sheet.write(0, 34, '')

        # 29 预定office,可为空
        res_sheet.write(line_num, 34, 'PEK302')
        # 是否支持代码共享航班
        res_sheet.write(line_num, 35, '非共享')
        # 是否支持经停航班
        res_sheet.write(line_num, 36, '全部')
        res_sheet.write(line_num, 37, cpa_type)
        res_sheet.write(line_num, 38, cpa_proportion)
        res_sheet.write(line_num, 39, 0)
        res_sheet.write(line_num, 40, 20)
        res_sheet.write(line_num, 41, cpc_refund_rules)
        res_sheet.write(line_num, 42, cpc_change_rules)
        res_sheet.write(line_num, 43, str_change)

        res_sheet.write(line_num, 44, '投放')

        res_sheet.write(line_num, 45, 30)
        line_num += 1
        if line_num == 65536:
            sheet_num += 1
            line_num = 1
            res_sheet = workbook.add_sheet('%sprepay%d' % (company.lower(), sheet_num))
            pre_sheet(res_sheet)
    workbook.save(r'/data/download/%s_prepay.xls' % company.lower())


def create_zipfile(company):
    z = zipfile.ZipFile(r'/data/download/%s_prepay.zip' % company.lower(),
                        mode='w', compression=zipfile.zlib.DEFLATED)
    z.write(r'/data/download/%s_prepay.xls' % company.lower(),
            './%s_prepay.xls' % company.lower())


def cy_xls(company):
    if company:
        res_sheet, dateFormat, workbook = init_execl(company)
        get_detail(company, res_sheet, workbook, dateFormat)
        create_zipfile(company)


def main():
    cy_xls("TV")
    # pass


if __name__ == '__main__':
    main()
