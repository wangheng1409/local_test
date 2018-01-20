import sys
import re
from lxml import etree
import base64
import chardet

# reload(sys)
# sys.setdefaultencoding("utf-8")

# import requests
# headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36"
#     }
# a = requests.get(url='http://proxydb.net/?offset=0', headers=headers)
#
# # a = str(a.text)
# # tree = etree.HTML(a)
# # node_list = tree.xpath("//table/tbody/tr")
# # for one in node_list:
# #     ip_str = one.xpath("td[1]")[0].xpath('string(.)')
# #     step2 = re.findall(r"atob\('(.*?)'.replace", ip_str, re.MULTILINE)
# #     print step2[0]
# #     print chardet.detect(step2[0])
# #     print base64.b64decode(str(step2[0]))
#
# print(a.content.decode())

import execjs
import base64
json_raw='''function a(){
var o = '1.631.312'.split('').reverse().join('');
var yy = '\x4d\x44\x55\x75\x4e\x6a\x49\x3d'.replace(/\\x([0-9A-Fa-f]{2})/g,function(){return String.fromCharCode(parseInt(arguments[1], 16))});
var pp = -55254 + 58382;
return [o , yy , String.fromCharCode(58) , pp]
}'''
jsn = execjs.compile(json_raw).call('a')
print(jsn)
jsn[1]=base64.b64decode(jsn[1]).decode()
print(jsn)
print(''.join([str(x) for x in jsn]))