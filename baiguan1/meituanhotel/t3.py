import requests

def headers(page,city):

    url='http://hotel.meituan.com/api/getcounterandpois/'+str(city)+'?ci=2017-06-14&co=2017-06-15&sort=&w=&page='+str(page)+'&attrs='
    momo_headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cookie': 'rvct=1; __mta=143520394.1494907759764.1494907767293.1494907796393.3;'
                  ' iuuid=AC9523D9E829A9B952C338A7CC8694D521FD5A493119AC4A239B935618FCC71D;'
                  ' IJSESSIONID=19g02ayyw148xeshxxsc1xy7n; ci3=1; a2h=1; ci=1; cityname="%E5%8C%97%E4%BA%AC";'
                  ' i_extend=C_b1Gimthomepagecategory1394H__a; abt=1497410937.0%7CADE; _lxsdk_cuid=15ca4a5ae9cc8-0fef562838cd6c-14386d5d-384000-15ca4a5ae9dc8;'
                  ' hotel_ci=10; _lxsdk_s=15ca4a5ae9f-065-36d-300%7C%7C11; __utma=211559370.215373552.1497410953.1497410953.1497410953.1;'
                  ' __utmb=211559370.10.10.1497410953; __utmc=211559370; __utmz=211559370.1497410953.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none);'
                  ' uuid=1f3dcbe13a9e63ea2290.1494907751.0.0.0; '
                  'oc=bq-gdKFvntLCX5J9vcPsdmbuJdHvi7GH36MvQdDpxvoqfpi7bGwJAwbZSdKoG8KOAR_BXLzgPVRaYfGmJQGOgYZ9XF2RBFDm-MNFu-SHd6CCbM5n3DBnV_lx-F9VdUnLR-UyyBKpPutAsZGc2-RjezByt7m36jYKq8lfwiJ9RPY',
        'Host': 'hotel.meituan.com',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://hotel.meituan.com/search/jiudian/shanghai?search=1&mtt=1.hotel%2Fdefault.0.0.j3wgti3l',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    return  url,momo_headers

#
if __name__ == '__main__':

    url,headers = headers(210,'shanghai')
    print(requests.get(url, headers=headers,verify=False).text)