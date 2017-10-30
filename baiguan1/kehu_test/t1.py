import requests
import random

def headers(name_id,page):
    url='https://whalewisdom.com/stock/holdings?id='+str(name_id)+'&q1=-1&change_filter=&mv_range=&perc_range=&rank_range=&sc=true&_search=false&rows=25&page='+str(page)+'&sidx=name&sord=asc'
    momo_headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.8',
        'cache-control': 'max-age=0',
        'cookie': 'recent_stocks=175032%2C133672; search_filter=6; _ga=GA1.2.183643219.1497322584; _gid=GA1.2.956927273.1497322584',
        'if-modified-since': 'Fri, 13 Jan 2017 15:34:28 GMT',
        'if-none-match': 'W/"'+random_ssid()+'"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36'
    }
    return  url,momo_headers

def random_ssid():
    return ''.join(
        map(lambda i: chr(random.randint(97, 122)) if random.randint(1, 4) in [1, 2] else str(random.randint(0, 9)),
            range(32)))

#
if __name__ == '__main__':

    url,headers = headers(175032,1)
    print(requests.get(url, headers=headers).text)
