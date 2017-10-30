# !/usr/bin/env python
# -*- coding:utf-8 -*-

def do_response(self, response):
    page = response.meta['page']
    ci = response.meta['ci']
    cf = response.meta['cf']
    url = response.meta['url']
    filters = response.meta['filters']
    header = response.meta['header']
    if response.status == 403:
        yield scrapy.Request(url=url,
                             headers=self.header,
                             callback=self.do_response,
                             dont_filter=True,
                             errback=self.errback_httpbin1,
                             meta={
                                 'page': page,
                                 'ci': ci,
                                 'cf': cf,
                                 'url': url,
                                 'filters': filters,
                                 'header': header,
                                 'handle_httpstatus_list': [403]
                             })
        return
    left = response.text.index('{')
    tmp = response.text[left:].strip()[:-2].replace(' ', '').replace('"}"', '""').replace('\\', '') \
        .replace('{"', '#@1').replace('":"', '#@2').replace('":', '#@3').replace('","', '#@4') \
        .replace(',"', '#@5').replace('"}', '#@6').replace('["', '#@7').replace('"]', '#@8') \
        .replace('"', '') \
        .replace('#@1', '{"').replace('#@2', '":"').replace('#@3', '":').replace('#@4', '","') \
        .replace('#@5', ',"').replace('#@6', '"}').replace('#@7', '["').replace('#@8', '"]')
    try:
        goods_dic = json.loads(tmp)
    except Exception as e:
        print(e)
        print(tmp)
        return

    goodsCount = goods_dic['goodsCount']
    all_page = goodsCount // 120 + 1
    if all_page > 50:
        start_cf = copy.deepcopy(cf)
        index = len(start_cf.split(','))
        for cf in filters[index]:
            cf = start_cf + ',' + str(cf)
            url = self.url % ('0', cf, ci)
            header = copy.deepcopy(self.header)
            header.update({'Referer': 'https://m.suning.com/list/' + str(ci) + '-' + str(0) + '.html', })
            yield scrapy.Request(url=url,
                                 headers=header,
                                 # cookies=cookie,
                                 callback=self.do_response,
                                 dont_filter=True,
                                 errback=self.errback_httpbin2,
                                 meta={
                                     'page': 0,
                                     'ci': ci,
                                     'cf': cf,
                                     'url': url,
                                     'filters': filters,
                                     'header': header,
                                     'handle_httpstatus_list': [403]
                                 })
    else:
        dic = {
            'ci': ci,
            'cf': cf,
            'all_page': all_page,
            'page': -1
        }
        self.r.lpush(self.redis_key, json.dumps(dic).encode("utf-8"))
        pp.append(dic)
        print(pp)