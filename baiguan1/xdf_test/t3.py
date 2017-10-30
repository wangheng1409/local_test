import requests
import re
import datetime
import time
tomorrow=str(datetime.date.today() + datetime.timedelta(days=1))
s=requests.get(url='http://souke.xdf.cn/Class/1-2945009.html').text
CityId=re.findall('sid: (\d+),',s)[0]
SchoolId=CityId
CourseCode=re.findall('courseId: "1-(\d+)",',s)[0]
ClassId=re.findall('classId: (\d+),',s)[0]

print(CityId,SchoolId,CourseCode,ClassId)
page=0
url='http://souke.xdf.cn/Class/CourseOtherClass?' \
    'CityId='+CityId+'&' \
    'SchoolId='+SchoolId+'&' \
    'CourseCode='+CourseCode+'&' \
    'ClassId='+ClassId+'&' \
    'Sort=0&' \
    'Hide=1&' \
    'ApplyState=1&' \
    'MinDate='+tomorrow+'&' \
    'MaxDate=3000-01-01&' \
    'MinPrice=0&MaxPrice=10000000&' \
    'BusinessDistrictCode=&' \
    'AreaCodes=&' \
    'ClassTimeCode=&' \
    'ClassModeCode=&' \
    'ClassCapacityCode=&' \
    'TeachingContentCode=&' \
    'BookVersionCode=&' \
    'PageNumber='+str(page)+'&' \
    'PageSize=5&' \
    '_='+str(int(time.time()))

head={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cache-Control':'max-age=0',
'Host':'souke.xdf.cn',
'Proxy-Connection':'keep-alive',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
}
print(url)
print(requests.get(url=url,headers=head).text)