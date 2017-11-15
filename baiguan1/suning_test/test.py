# !/usr/bin/env python
# -*- coding:utf-8 -*-
# app_df={'1':('android','xiaomi'),'2':('ios','apple'),'3':('Symbian','nokia'),}
#
# s={ k: v   for key,row in app_df.items() for k,v in zip([x+'_'+key for x in ['app','app_name']],row)}
# print(s)

s=set()
s.add('爱上租')
s.add('自如')
s.add('青客')
s.add('蘑菇公寓')
s.add('蛋壳公寓')
s.add('安心公寓')
s.add('水滴公寓')
s.add('优客逸家')
s.add('蜜柚公寓')
s.add('寓见')
print(len(s))