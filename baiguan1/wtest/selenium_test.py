from selenium import webdriver
browser=webdriver.PhantomJS('./phantomjs')
# browser=webdriver.Chrome('/Users/go/Downloads/chromedriver')
browser.get('https://h5.m.taobao.com/app/waimai/index.html?locate=icon-4&spm=a215s.7406091.icons.4&scm=2027.1.2.10021#')
browser.implicitly_wait(20)
html=browser.page_source
print(html)


