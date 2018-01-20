# !/usr/bin/env python
# -*- coding:utf-8 -*-


class CutByPrice:
    async def handle(self,response,split_str,cf,deal_core,next_url,*args,**kwargs):
        '''
        
        :param response: a html or a json
        :param split_str: cutting mark
        :param cf: the result of the cutting
        :param deal_core: 处理respnse的协程
        :param next_url: 最终发请求的协程
        :param args: 
        :param kwargs: 
        :return: 
        '''
        filters = []
        a, b = cf.split(split_str)
        if (int(b) - int(a)) == 1:
            filters.append(a + split_str + a)
            filters.append(b + split_str + b)

        elif (int(b) - int(a)) == 0:
            await deal_core()
        else:
            filters.append(a + split_str + str(int(a) + (int(b) - int(a)) // 2))
            filters.append(str(int(a) + (int(b) - int(a)) // 2) + split_str + b)
        for cf in filters:
            await next_url(cf)





for x in 'a=1,b=2,c=3'.split(','):
    print(x)
    for k, v in x.split('='):
        print(k,v)