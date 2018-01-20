# !/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import requests
import time


url='http://wmapi.meituan.com/api/v8/poi/food?' \
    'utm_term=6.0.3&' \
    'utm_source=2000&' \
    'platform=5&' \
    'wm_actual_longitude=116418512&' \
    'waimai_sign=lCYoYyG28Kj3tM4UKCHuc6SihC5kFP7z4krOcHcv%2Brgj4Hnt3CZLt5FbtVgvspPUDh7qW4VLpalmKd319eiX6ImuqzbZSWiuihlPCGwRGUmbW1YB43aLLLfxFO8E%2FErx5vQTopP%2B5hRgSBtEDrQFuM2HYZLzFeDesO8BJjoagQ8%3D&' \
    'partner=4&' \
    'version=6.0.3&' \
    'req_time=1512358166012&' \
    'uuid=5DC0518B391B6AC740961C1549E1576752EF89A47875CC6D76162EBCDB424057&' \
    'wm_dversion=10.0.2&' \
    'wm_visitid=FB8F40B5-BA41-4EF2-AA40-70EB22C07B902017-12-04-11-20619&' \
    'wm_actual_latitude=39948380&' \
    'app=4&' \
    'wm_seq=43&' \
    '__skno=CC7F0067-AF44-46B1-9946-83FE81A2576A&' \
    'wm_appversion=6.0.3&' \
    'wm_ctype=iphone&' \
    '__skcy=rkNd466X7QA1zbYlVPdejBG7Rds%3D&' \
    'utm_medium=iphone&' \
    '__skua=9144754a01d5e83dc4e60643d42b7784&' \
    'wm_logintoken=&' \
    'wm_dtype=iPhone%206&' \
    'wm_did=00BAD454-B0F1-4156-8D41-773DC84D2D43&' \
    'wm_channel=2000&' \
    'ci=1&' \
    '__skck=3c0cf64e4b039997339ed8fec4cddf05&' \
    'wm_uuid=5DC0518B391B6AC740961C1549E1576752EF89A47875CC6D76162EBCDB424057&' \
    'wm_longitude=116418512&' \
    'movieBundleVersion=100&' \
    'utm_content=5DC0518B391B6AC740961C1549E1576752EF89A47875CC6D76162EBCDB424057&' \
    '__skts=1512358166.113464&' \
    'wm_latitude=39948380&' \
    'utm_campaign=AwaimaiBwaimaiGhomepage_poilist_0_1897048H0' \
    '&userid='

headers={
    'Host': 'wmapi.meituan.com',
    'X-SAKHTTPCache-IgnoreQueryKey': '__reqTraceID',
    'Accept': '*/*',
    'pragma-unionid': '74c31d81861c4eb5af41aa99786cb9ed0000000000000710564',
    'Accept-Encoding': 'gzip, deflate',
    'pragma-os': 'MApi 1.1 (mtscope 6.0.3 appstore; iPhone 10.0.2 iPhone7,2; a0d0)',
    'Accept-Language': 'zh-Hans-US, en-US, en-us;q=0.8',
    'X-SAKURLCandyPolicy': '123',
    'User-Agent': 'com.meituan.itakeaway/4215 (unknown, iOS 10.0.2, iPhone, Scale/2.000000)',
    'siua':'Rt1u+F4kXJ0wS8wE2G19F/4FzDlKppaBo23uPmx4WselQeg+HHZxVQQebqOHM5GhXhzcA0ePWWWPd6Yb0/2xTV3PHq/OtyihSynpFZxWd1bLB3SdMJ0FDoHZPUQd83WR2JPZ5JvC2ReO2mtiyuB/jhvf+sW/OugJ6eA7ixrtQ4Q4ePhlaeDsLvR/z0tfqQh1aw51k0nlJZ0QXhDgOLcPLYgs4qcePHZ3gbeJALBCaiiNnYtNzpqUU4RxdTGVp95C8vD9i6C5QCeYaTiMEZlZBIhQIXkfzgPK03LtT89E6evat0Moa3W6NspuRqGQYN93atWTp0Nfu3WS5VsB6Bkt8bXbPdzEob7r8mc/dLf7Hel40qjJRSkootKh9IwaUSxO8C3HdGyxFfNZtT5KTT59PK4EVhJyFlyTyWu30KYPC1ri/LkWl5z84tKFy1Uc9KHWeIkXytXrAWjGz1L/Ta7Rzsja2YOkzIEFzMfYi68r3WNK2M1EAq3IbMXwFlhldghIbUSr8ejfu69yo7Tke63sV5IOre7PnWI+Oywh9ybewCSpnH1X9FnTjRo/sAdGGG99NQfqojLkLOUGRshL970/wh9tuZ2q1MbFAgH0l8YhrxA=',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
}
data={
   'fingerprint'	:'i2HKpOmsirDPavelVfQBZIVxBuyhIb/j2DtCdTkUeCqoFHJPYoHM7D5l6TvAL9e7q+WvKqMsb5HtdUXg8ThX3/SV4Mi/0wAjNfO+eBXnVMEjqBL+0sRg7d0amkJ8J3Kpe9F0MG4fwnzjZQDykVHg9XjWcs+GpypIRMe0UlF/ZVnwM55gyTrIBG05+JblrTBw9fwlvU1d+AMM/pCfGO4UPE88XenJrYmpVp/4tIMREoXoAxM8OZMndqxXJ5m1ZH5vGwELO9a2XRr4l/RLJJZOPdRWrL4YXtBfdjZz+tBjvmfoPtVbi1wWc1bQDWXArd/cjb+W1w+78HVtfCKE/7hArSL7LOKcQW7hk4AaKb1R5mmyjhWRzIAAXGxaLmuyWQRpIuarG5hUAHSksmI8kjPVDQbCbRHNHrn0cGrBqV3tZPsLlnt9I6F5OE1N13Vs6En2zm88Tc63UtOy2CZ63BRixttOWVUtwEYUcTwI9jW0pE/MtDYofbzaLwPbSwJpoClr2kLdmpXvPw4Ks3QrB0mqww7otimn8jkXFk07SChR+k3vE0m4xF6lhkDh4NpXOQwZrJYXYSL0SEM5+xGWJfB1a7gYe5Q8e7Oc+BfcIGYBNyyCxM5p+zkHXJs5y2cCMiSh2F4IjAOuHbeNV6dLOOdhDjeuxhrR//v4UF36heOqIRcxBqIX4RGqIer7qcd8BuOF9m2KvYFkm9fWUbWX7s2TQ4gJ6+UzK0n/K0bmFOXNYSgTxkq4Njn8dTG7DkvJaalPXT9PNuNOEhevCkmj/70Em7Vk5K30Uu0QRIwT2X3OEj7g7dDA1kCWFsQVjwpV7blg0biYtUGF6tfqMQFSGRnFmiYlp05EVnEmlqm8jtRfcOlVmWhcAYdadlVVDY4h3AJeL0RXO3Lcq2mr3WwNXNGWS6G1qcUepG2/xel700CPPqtFJ8/nJOv5dynf7/j21fjGb4aenTQt08hXWu/Xp3UVr5VjpMEfsCgRjKkhPW8Y9ka0c2ShO4QEMMqowzq9f0dOA4CaQCcLz0MevRiouxPt+BZMXSyPdvraTgIAK9MdzMqgVDQZbZ8sMgxITQas7P/7a2JOLkTdMU+ji6DwJX8nZnySKgcuctBy/lU2s6rjqb/cJfkvgsA73R3OKLtVNnHC70ANFjLHlAyYh1EQ+iaIng==',
    'page_index'	:'0',
    'trace_tag'	:'{"action":"click","src_item_id":"1897048","tgt_page":"p_poi","extra":{"has_clicked_spu":"0","ad":{"adType":0,"adChargeInfo":{}},"friend_comment":"2"},"src_page":"p_homepage","src_block":"b_poilist","tgt_block":["b_shoppingcart","b_increase","b_decrease","b_food_area"],"req_time":"1512358165793","src_item_index":"0"}',
    'wm_fingerprint':	'X5IG7izeH9Q9TlTqqFrjewYAQISbuBle7vfQdXdSYJbW/3L84t/y+uwTfvnw+QY0C/UDDNUKSLr9rsSOuertBT2DdvwucJqXGGHV4tQN6FCouKKblOUBcdHLgJYPZzJMbmTXAUSdVaVjgbfgiKe1WTUD5V2RInpGwvW2yiZVH+hw8oLmhr62HHO2qto6HjUWLx94rDd0fY7WAwrb4ybj+ncX5ZSe4NoFmWP+9tqDr4A151qr01JQXdaMHOWRop0CYqWZV/GmvfRYLROSdao6RBpk6DAh3N89M5WTABn4WSHecl2TO0pzcOQyRh6Yh5tFJaPcJAloSJ2BfRfskdwnLJTIDuI9mCz96zhK0OtR1uTPnduZJQQm2w6O0VZ4Q3X/7fzdXGVjc4DJZc+zp2kO3DchEQTDAaVtfBjJfiXnW0Tws+RT68aUoX0E9RDxFDIro57UWOseRERqKs71BuqwR/zB6RlRCVu+q7DFbX3sNVHGn7keLc4AEn+s7owFkOIF3PMpgX8Z0taNHUTbFI/MILmNJzenLjV981rWVU2XlzSJKJ/aZjBdltuA25TriozgrDBiFiR3Pc9ez0xDkXKo4ZNUz2MW9OnGpLU2y5BdXsJONSVTZQkCKmh9D9GpvqqQAPE7tgHimsV3rwBmwAZGqBjAQt5VKTgu26PpcGv3lnOmsTLb4KNqx54g65x0Rtd0m2JOpXqOhHjgHwQho0vpwWFLeuoxiQdi4462Hmu3JECdt7mQILLB3KGcsm/9C4llh5WvdS8Xs1t4zwuy9+ln6lNOFh91K8XmV+SEHQnqQvT1Ihg3nU94oGQWgVPXGKLcoKXx3IlfbISH1HaGpEpX3krNIeX5xybomnFVnyJyaTVX8btJWOn9B3ykTSTY3DWdtJWX7KdpzxatRNCpJWLW5WQ/7D7NIrR4+esnfgI6Jugd/qhcwhGUrcbvaU7l7eUU/V27EW/nqENII2GjBl9Z3GxVmR8xX0LQY9XhW6aMEtcDnelyLtD30We6vsDgOPYeIrSrukkOaAEoHkZKm5WgLUPtcKtte4fWHkDtqoKaYrMXTpAwfMErNoTavT9+Sljjcq4rnUACJCWB15XVI2ZbQOvaEvGrE44/E2LKvq29CFXWnUeh1HoGPd9AlHhFwhFsMkW1lWiktNkfEhLc6whXr224JRq7KPWfPQ0f5Mnrk/FKRTVUiu9Ir3gu3CldeQTTL5wLIAin+WBNPL6roK+FGE6Ql/qRiDOyV3T5Ah6Qat+lJnBYZ/Hh/42lWsSsI+COxxsuTdvDHQ501zPFP899bSUcbwAvpld1sBg0sOaAaUBQff49kgz/qSqt89loK1o8YqLf+KDyFCeFrSzfppLuOGHVOisIFvddeQ1z3qYT7B7oI21aW8vYSg0eOj7zkcMGF74QQFLUfSQ=',
    'wm_poi_id'	:'1897048',
}

ret=requests.post(url,headers=headers,data=data).text
print(ret)









