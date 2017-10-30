import requests
import random
headers = {
    'Connection': 'keep-alive',
    'Host': 'p.grabtaxi.com',
    'User-Agent': 'GrabTaxi/4.27.1 (iPhone; iOS 9.0.2; Scale/2.0)',
    }
ret=requests.get('https://p.grabtaxi.com',headers=headers)
print(ret.text)