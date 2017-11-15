# !/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import requests
import time


url='http://www.dankegongyu.com/room/bj?page=274'

headers={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    # 'Cookie': 'LXB_REFER=www.google.com; _ga=GA1.2.383380687.1509600382; _gid=GA1.2.1263284930.1509600382; XSRF-TOKEN=eyJpdiI6IkJmMU9Sd21TRmFCM2xHOFE4MG1JNUE9PSIsInZhbHVlIjoicEVVVXVGZm1ldFpiUmtHMVdLQytZUEdCd1BcL092ejBhc2tGUjNcL1I5aG42c1BsemU3bEphMldwY1VQRVZkRjI4YzFDWDJnSERZYjdkdGpTeDUrdHI3Zz09IiwibWFjIjoiY2UxYTQwYzBhODdhMGFkNjc5ZGU4MTk1MDY3MjBiMjliM2IyN2ZiZjQ1ZGRlYmU3ZDQwNTg3MWRlNjA4MTIzNiJ9; session=eyJpdiI6IkUrMTNXUUloSk1YeUZqRHhoaVwvOVdBPT0iLCJ2YWx1ZSI6IlU2RXlaS2d4dVg0SVdpNGh3Q2VWRUJ4Ynp2cDg3XC9GcGMyaDgzWHRqUHo3bnV3MVh5WFdGR3A0NXBybjRieVJlRGVpYzZuRllLS2hET2srM3k3ZlQydz09IiwibWFjIjoiMTkwNGIyMDEyMmI4NTgwNzhjMzY2OGMzNzEzNjQ2N2MwNTZkNjU5YTRjYzRlNTEyYWM5YWM5ZjA1ZTk0MDc1MiJ9; Hm_lvt_814ef98ed9fc41dfe57d70d8a496561d=1509600383; Hm_lpvt_814ef98ed9fc41dfe57d70d8a496561d=1509600549',
    'Host': 'www.dankegongyu.com',
    'Referer': 'http://www.dankegongyu.com/room/bj?page=275',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
}

ret=requests.get(url,headers=headers).text
print(ret)

