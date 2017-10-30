# -*- coding: utf-8 -*-

STORE_ITEM_STATUS = [
    ('new', u'新增商品'),
    ('pending_review', u'待审核'),
    ('human_verified', u'已通过人工审核'),
    ('auto_verified', u'已通过自动审核'),
    ('no_matches', u'没法匹配'),
    ('na', u'不处理'),
    ('error', u'数据有误'),
]

STANDARD_ITEM_STATUS = [
    ('new', u'新增标品'),
    ('pending_review', u'待审核'),
    ('half_verified', u'半审核'),
    ('human_verified', u'已通过人工审核'),
    ('auto_verified', u'已通过自动审核'),
    ('na', u'不处理'),
]

STANDARD_ITEM_SOURCE = [
    ('barcode_store', u'条码店'),
    ('food_safety', u'食品安全官网'),
]

STANDARD_VENDOR_STATUS = [
    ('new', u'新增条码'),
    ('pending_review', u'待审核'),
    ('human_verified', u'已通过人工审核'),
    ('na', u'不处理'),
]

STANDARD_VENDOR_SERIES_CATEGORY = [
    ('pending_review', u'待审核'),
    ('human_verified', u'已通过人工审核'),
    ('na', u'不处理'),
]

STORE_BUSSINESS_HOURS = [
    ('day', u'日营业'),
    ('24hours', u'24小时'),
]

STORE_SCALES = [
    ('small', u'小型超市'),
    ('medium', u'中型超市'),
    ('big', u'大型超市'),
    ('super', u'百货超市'),
]

STORE_RECEIPT_PRINTING_FREQUENCE = [
    ('all', u'所有'),  # 打所有的
    ('often', u'经常'),  # 烟酒, 水, 小量的不打
    ('occasionally', u'偶尔'),  # 沒打小票的習慣
]

STANDARD_TAG_TYPE = [
    ('brand', u'品牌'),
    ('series', u'系列'),
    ('category', u'商品分类'),
    ('property', u'商品属性'),
    ('quantity', u'商品数量'),
    ('ignore', u'忽略'),
]
STORE_WEEK = [
u'一',u'二',u'三',u'四',u'五',u'六',u'日'
]
# STANDARD_ITEMS_CATEGORIES = [
#     (u'tea', u'茶饮料类'),
#     (u'protein_drinks', u'蛋白饮料类'),
#     (u'powdered_drinks', u'固体饮料类'),
#     (u'juice', u'果汁及蔬菜汁类'),
#     (u'water', u'瓶（桶）装饮用水类'),
#     (u'other_drinks', u'其它饮料类'),
#     (u'coffee_milktea', u'咖啡/奶茶'),
#     (u'soft_drinks', u'碳酸饮料（汽水）类'),
#     (u'fast_food', u'方便食品'),
#     (u'biscuit', u'饼干糕点')
# ]

# STANDARD_ITEMS_CATEGORIES_DICT = dict(STANDARD_ITEMS_CATEGORIES)

# COCACOLA_FOCUS_CATEGORIES = dict([
#     (u'tea', u'茶饮料类'),
#     (u'juice', u'果汁及蔬菜汁类'),
#     (u'water', u'瓶（桶）装饮用水类'),
#     (u'other_drinks', u'其它饮料类'),
#     (u'soft_drinks', u'碳酸饮料（汽水）类'),
# ])

ENTITY_TYPE_CHOICES = [
    ('0501|0502|0503|0504', u'餐饮场所'),
    ('1906', u'标志性建筑物'),
    ('1907', u'热点地名'),
    ('1905', u'市中心'),
    ('01|02|03', u'汽车相关'),
    ('20', u'公共设施'),
    ('1502', u'火车站'),
    ('1503', u'港口码头'),
    ('1501', u'机场相关'),
    ('1506', u'轻轨站'),
    ('1507', u'公交车站'),
    ('1504', u'长途汽车站'),
    ('1505', u'地铁站'),
    ('1508', u'班车站'),
    ('1509', u'停车场'),
    ('060101', u'购物中心'),
    ('060103', u'免税品店'),
    ('060102', u'普通商场'),
    ('0614', u'个人用品/化妆品店'),
    ('13', u'政府机构及社会团体'),
    ('17', u'公司企业'),
    ('16', u'金融保险服务'),
    ('18', u'道路附属设施'),
    ('0801', u'体育休闲服务'),
    ('0602', u'便民商店/便利店'),
    ('0603', u'家电电子卖场'),
    ('1102', u'风景名胜'),
    ('0607', u'综合市场'),
    ('0604', u'超级市场'),
    ('1101', u'公园广场'),
    ('1411', u'传媒机构'),
    ('1412', u'学校'),
    ('1413', u'科研机构'),
    ('1414', u'培训机构'),
    ('1415', u'驾校'),
    ('1201', u'产业园区'),
    ('1203', u'住宅区'),
    ('1202', u'楼宇'),
    ('07', u'生活服务'),
    ('04', u'摩托车服务'),
    ('0606', u'家居建材市场'),
    ('0612', u'专卖店'),
    ('0611', u'服装鞋帽皮具店'),
    ('0610', u'特色商业街'),
    ('1401|1402|1403|1404|1405|1406|1407', u'科教文化场馆'),
    ('0605', u'花鸟鱼虫市场'),
    ('0901', u'医疗保健服务'),
    ('0505|0506|0507|0508|0509', u'休闲餐饮场所'),
    ('1510', u'过境口岸'),
    ('0608|0609', u'文体用品店'),
    ('1002', u'旅馆招待所'),
    ('1001', u'宾馆酒店'),
]
ADVERTISEMENT_STATUS_CHOICES = [
    ('under_approved', u'审核中'),
    ('disapproved', u'审核失败'),
    ('wait_for_enabling', u'等待启用'),
    ('wait_for_advertising', u'等待投放'),
    ('advertising', u'正在投放'),
    ('advertise_finished', u'投放结束'),
]

ADVERTISER_TYPE_CHOICES = []
