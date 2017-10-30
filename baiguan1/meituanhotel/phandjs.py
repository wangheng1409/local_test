# !/usr/bin/env python
# -*- coding:utf-8 -*-
from selenium import webdriver
service_args = ["--proxy=123.59.69.66:8081", '--ignore-ssl-errors=true']
webdriver.DesiredCapabilities.PHANTOMJS[
    'phantomjs.page.customHeaders.User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
driver = webdriver.PhantomJS('./phantomjs', service_args=service_args)

# 加载网页
driver.get("https://www.baidu.com")
# 测试加载结果，输出标题
print(driver.)
