# !/usr/bin/env python
# -*- coding:utf-8 -*-
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver

htmlunit = webdriver.Remote(desired_capabilities=DesiredCapabilities.HTMLUNIT)
htmlunit.get("http://www.baidu.com")
print (htmlunit.title)