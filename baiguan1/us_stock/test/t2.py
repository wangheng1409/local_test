import requests

import time


url='https://whalewisdom.com/filer/acadian-asset-management-llc'

headers={
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
}

ret=requests.get(url=url,headers=headers,verify=False).text
print(ret)