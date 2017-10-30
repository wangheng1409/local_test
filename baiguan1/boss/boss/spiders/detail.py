# -*- coding: utf-8 -*-
import scrapy
import json
import datetime
import time
import redis
import re
from scrapy_redis.spiders import RedisSpider
from scrapy.conf import settings
from boss.items import BossItem,BossCompanyItem
from boss.before.before import headers


class StockSpider(scrapy.Spider):
    name = "bossspider"
    domain ='https://www.zhipin.com/'
    city_dict={}
    company_set=set()
    def start_requests(self):
        yield scrapy.Request('https://www.zhipin.com/',headers=settings['HEADER'],callback=self.parse,dont_filter=True)

    def parse(self, response):
        self.city_dict={a:b for a,b in zip(response.xpath('//div[@class="dorpdown-city"]//li[starts-with(@ka, "city")]/@data-val').extract(),
                     response.xpath('//div[@class="dorpdown-city"]//li[starts-with(@ka, "city")]/text()').extract())}
        left_list=[re.findall('p(\d+)',x)[0] for x in response.xpath('//div[@class="text"]//a/@href').extract()]
        for city_code in list(self.city_dict.keys())[:1] if settings['TEST'] else list(self.city_dict.keys()):
            for left_code in left_list[:1]:
                url='/c%s-p%s'%(city_code,left_code)
                yield scrapy.Request(url= 'https://www.zhipin.com'+url,headers=settings['HEADER'],callback=self.detail_type,dont_filter = True)

    def detail_type(self,response):
        #排序         s_303 - y_4 - t_803
        #规模 s_
        g_list=[x[-3:] for x in response.xpath('//dl[@class="condition-scale"]//a[starts-with(@ka, "sel-scale-30")]/@ka').extract()]
        #融资 t_
        r_list=[x[-3:] for x in response.xpath('//dl[@class="condition-stage"]//a[starts-with(@ka, "sel-stage-80")]/@ka').extract()]
        #薪资 y_
        x_list=[x[-1] for x in response.xpath('//dl[@class="condition-salary"]//a[starts-with(@ka, "sel-salary-")]/@ka').extract()][1:]

        for g in g_list  if settings['TEST'] else g_list:
            for r in r_list if settings['TEST'] else r_list:
                for x in x_list if settings['TEST'] else x_list:
                    ur='/s_%s-y_%s-t_%s/?page=1&ka=page-1'%(g,x,r)
                    yield scrapy.Request(url=response.url + ur,headers=settings['HEADER'], callback=self.detail, dont_filter=True)

    def detail(self,response):
        # ret=response.content.decode()
        if '请输入验证码' in response.text:
            return scrapy.Request(url=response.url,headers=settings['HEADER'], callback=self.detail, dont_filter=True)
        if not response.xpath('//div[@class="job-list"]//li'):
            return
        for li in response.xpath('//div[@class="job-list"]//li')  if settings['TEST'] else response.xpath('//div[@class="job-list"]//li'):
            try:
                item = BossItem()
                s = {}
                s['url'] = 'https://www.zhipin.com' + li.xpath('./a/@href').extract()[0]
                s['name'] = li.xpath('./a//div[@class="info-primary"]/h3/text()').extract()[0]  # 职位名
                s['money'] = li.xpath('./a//h3/span/text()').extract()[0]  # 薪资
                cye = li.xpath('./a//div[@class="info-primary"]/p').extract()[0]
                s['city'] = li.xpath('./a//div[@class="info-primary"]/p/text()').extract()[0]
                s['years'] = re.findall('</em>(.*?)<em', cye)[0]  # 要求工作年限
                s['education'] = re.findall('</em>(.*?)</p', cye.split('class')[-1])[0]  # 教育背景

                s['company'] = li.xpath('./a//div[@class="company-text"]/h3/text()').extract()[0]  # 发布公司名

                pj = li.xpath('./a//div[@class="job-author"]/p').extract()[0]
                s['person'] = li.xpath('./a//div[@class="job-author"]/p/text()').extract()[0].split()[0]  # 发布人
                s['job'] = re.findall('</em>(.*?)<img', pj)[0]  # 发布人职位

                iwp = li.xpath('./a//div[@class="company-text"]/p').extract()[0]

                s['industry'] = li.xpath('./a//div[@class="company-text"]/p/text()').extract()[0]  # 行业
                s['wheel'] = re.findall('</em>(.*?)<em', iwp)[0]  # a轮
                s['people'] = re.findall('</em>(.*?)</p', iwp.split('class')[-1])[0]  # 公司人数

                s['tag'] = li.xpath('./a//div[@class="job-tags"]/span/text()').extract()[0].split() if li.xpath(
                    './a//div[@class="job-tags"]/span/text()') else []  # 岗位标签
                # s['release_time'] = li.xpath('./a//div[@class="job-time"]/span/text()').extract()[0].strip('发布于')  # 发布时间
                s['release_time'] = li.xpath('.//span[@class="time"]/text()').extract()[0].strip('发布于')  # 发布时间

                item['detail'] = s
                # if settings['TEST']:
                #     print(s)
                yield item
            except Exception as e:
                print(e,'sss1',response.url)

            if s['company'] not in self.company_set:
                self.company_set.add(s['company'])
                company_url=li.xpath('./a/@href').extract()[0]
                yield scrapy.Request(url='https://www.zhipin.com' + company_url,headers=settings['HEADER'], callback=self.job_detail, dont_filter=True)

        base_url=response.url.split('?')[0]
        page=str(int(re.findall('page=(\d+)', response.url.split('?')[1])[0])+1)
        burl=base_url+'?page=%s&ka=page-%s'%(page,page)
        yield scrapy.Request(url=burl, callback=self.detail,headers=settings['HEADER'], dont_filter=True)

    def job_detail(self,response):
        yield scrapy.Request(url='https://www.zhipin.com' + response.xpath('//div[@class="info-company"]/h3/a/@href').extract()[0],headers=settings['HEADER'], callback=self.company_detail, dont_filter=True)

    def company_detail(self,response):
        try:
            item=BossCompanyItem()
            s={}
            s['company_id']=re.findall('r(\d+)\.html', response.url)[0]
            s['company'] =response.xpath('//div[@class="company-banner"]//h3/text()').extract()[0]

            iwp = response.xpath('//div[@class="company-banner"]//p[1]').extract()[0]

            s['wheel'] = re.findall('p>(.*?)<em', iwp.split('class')[0])[0]  # a轮
            s['people'] = re.findall('</em>(.*?)<em', iwp)[0] # 公司人数
            s['industry'] = re.findall('</em>(.*?)</p', iwp.split('class')[-1])[0] # 行业
            s['com']=response.xpath('//div[@class="company-banner"]//p[2]/text()').extract()[0] if  response.xpath('//div[@class="company-banner"]//p[2]/text()') else ''#网址
            s['total_job']=response.xpath('//div[@class="company-stat"]//a/b/text()').extract()[0] #在招职位数量
            s['total_boss']=response.xpath('//div[@class="company-stat"]//span/b/text()').extract()[0] #boss数量

            item['detail'] = s
            # if settings['TEST']:
            #     print(s)
            yield item
        except Exception as e:
            print( e, 'sss2',response.url)


