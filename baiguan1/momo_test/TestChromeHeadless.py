#coding=utf-8
'''
Description:
    测试Chrome59，Headless模式，环境：MAC
    依赖：
        chrome, 直接从AppStore安装
        chormedriver, brew install chromedriver
        selenium, pip install selenium
Author:
    liuwen
Date:
    20170725
Ref:
    Splinter官网文档，参考Chrome59说明，但不使用splinter的样例代码
        http://splinter.readthedocs.io/en/latest/drivers/chrome.html
    使用 headless chrome进行测试:
        http://www.zhimengzhe.com/bianchengjiaocheng/qitabiancheng/301733.html
'''

from selenium import webdriver

# Chrome设置
ChromeOptions = webdriver.ChromeOptions()

# 设置参数
ChromeOptions.add_argument('window-size=1200x600')  # 窗口大小。不可见，最好人工设置。
ChromeOptions.add_argument("--disable-extensions")  # 不加载扩展。
# ChromeOptions.add_argument("--headless")            # 开启无头模式。即使是无头模式，也会开启Chrome浏览器，只是不会显式执行具体操作。

# 创建驱动
driver = webdriver.Chrome(chrome_options=ChromeOptions)

# 加载网页
driver.get("https://www.baidu.com")
# 测试加载结果，输出标题
print(driver.title)