import requests
from lxml import html
res=requests.get(url='http://souke.xdf.cn/Class/14-2099538.html')
response=html.fromstring(res.content)
ele_info_list = response.xpath('//div[@class="m-classdetails"]/dl[2]/dd/text()')[0]
print(ele_info_list)