# !/usr/bin/env python
# -*- coding:utf-8 -*-

print(len('71196706067541'))
print(len('70106119288977'))

import random
def oid_generator():
    # res = se.INITIAL+"%0.10d" % random.randint(0,9999999999)
    res = "%0.14d" % random.randint(0, 99999999999999)
    # res = '4'+"%0.11d" % random.randint(0, 99999999999)
    if len(str(int(res))) < 14:
        return oid_generator()
    else:
        return res


print([oid_generator() for i in range(100000) if len(oid_generator())<14])




s=[{'time': '2017-04-28 11:38:01', 'ftime': '2017-04-28 11:38:01', 'context': '已签收,签收人是员工通道', 'location': ''},
   {'time': '2017-04-28 10:17:07', 'ftime': '2017-04-28 10:17:07', 'context': '【浙江义乌公司】的派件员【彭想清】正在派件 电话:17769931957', 'location': ''},
   {'time': '2017-04-28 10:17:07', 'ftime': '2017-04-28 10:17:07', 'context': '【浙江义乌公司】已收入', 'location': ''},
   {'time': '2017-04-28 09:40:09', 'ftime': '2017-04-28 09:40:09', 'context': '快件已到达【浙江义乌公司】 扫描员是【北苑站点 D】上一站是【】', 'location': ''},
   {'time': '2017-04-28 08:49:11', 'ftime': '2017-04-28 08:49:11', 'context': '由【浙江义乌公司】发往【浙江义乌北苑营业部】', 'location': ''},
   {'time': '2017-04-28 08:45:32', 'ftime': '2017-04-28 08:45:32', 'context': '快件已到达【浙江义乌公司】 扫描员是【张慧2】上一站是【】', 'location': ''},
   {'time': '2017-04-28 01:55:54', 'ftime': '2017-04-28 01:55:54', 'context': '由【浙江杭州中转部】发往【浙江义乌公司】', 'location': ''},
   {'time': '2017-04-27 21:05:28', 'ftime': '2017-04-27 21:05:28', 'context': '由【浙江余姚公司】发往【浙江杭州中转部】', 'location': ''},
   {'time': '2017-04-27 20:44:22', 'ftime': '2017-04-27 20:44:22', 'context': '【浙江余姚公司】正在进行【装袋】扫描', 'location': ''},
   {'time': '2017-04-27 20:44:22', 'ftime': '2017-04-27 20:44:22', 'context': '由【浙江余姚公司】发往【浙江宁波中转部】', 'location': ''},
 {'time': '2017-04-27 18:13:10', 'ftime': '2017-04-27 18:13:10', 'context': '【浙江余姚公司】的收件员【公司现收】已收件', 'location': ''}]




























