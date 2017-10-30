import requests

url='http://it.snssdk.com/api/news/feed/v46/?' \
    'refer=1&' \
    'count=20&' \
    'max_behot_time=1500958282&' \
    'last_refresh_sub_entrance_interval=1501055162&' \
    'loc_mode=0&' \
    'tt_from=pre_load_more&' \
    'lac=0&' \
    'cp=55967a8c498baq1&' \
    'iid=12614533940&' \
    'device_id=35284694273&' \
    'ac=wifi&channel=sem_baidu_lite_ys&' \
    'aid=35&' \
    'app_name=news_article_lite&' \
    'version_code=583&' \
    'version_name=5.8.3&' \
    'device_platform=android&' \
    'ab_version=151496%2C146818%2C151121%2C150251%2C152151%2C153438%2C152355%2C152374%2C122834%2C152652%2C143763%2C144450%2C149167%2C151123%2C148467&' \
    'ab_client=a1%2Cc2%2Ce1%2Cf2%2Cg2%2Cf7&' \
    'ab_feature=z1&' \
    'abflag=3&' \
    'ssmix=a&' \
    'device_type=Coolpad+5263S&' \
    'device_brand=Coolpad&language=zh&' \
    'os_api=19&' \
    'os_version=4.4.4&' \
    'uuid=99000782206545&' \
    'openudid=5c9b7b644a86f8f&' \
    'manifest_version_code=588&' \
    'resolution=480*854&' \
    'dpi=240&' \
    'update_version_code=5833&' \
    '_rticket=1501055162117'

header={
'Accept-Encoding':	'gzip',
'User-Agent'	:'Dalvik/1.6.0 (Linux; U; Android 4.4.4; Coolpad 5263S Build/KTU84P) NewsArticle/5.8.3 okhttp/3.4.1',
'X-SS-REQ-TICKET'	:'1501055162123',
'Cookie'	:'install_id=12614533940; ttreq=1$6274858e1affe44906ceca5a90c498469739bea9; qh[360]=1',
'Host'	:'it.snssdk.com',
'Connection':	'Keep-Alive',
}

ret=requests.get(url,headers=header).content.decode(encoding='utf8').replace('\\','')
print(ret)