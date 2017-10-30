from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
t=time.time()
browser=webdriver.PhantomJS('./phantomjs')
# driver=webdriver.PhantomJS('./phantomjs')
#
browser.get('http://hotel.meituan.com/beijing')
browser.implicitly_wait(500)
html = browser.page_source
print(html)
print(time.time()-t)

# try:
#         element = WebDriverWait(browser,30).until(
#                 EC.presence_of_element_located((By.ID,"hotel-list-wrapper"))
#         )
#         html = browser.page_source
#         print(html)
# finally:
#     browser.quit()


