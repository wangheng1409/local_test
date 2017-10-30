import requests
import json
import time
yuan=[{'category': 'news_society', 'web_url': '', 'flags': 0, 'name': '社会', 'tip_new': 0, 'default_add': 1, 'concern_id': '6215497899397089794', 'type': 4, 'icon_url': ''}]
#1501113274
t=int(str(time.time()).split('.')[0])-1000
concern_id=6215497899397089794
category='live_talk'

url1='http://ib.snssdk.com/api/news/feed/v54/?resolution=640*1136&ab_feature=z1&vid=268E9FF9-A095-4656-B343-EB377C7CFA26&app_name=news_article&channel=App%20Store&openudid=c362770eef5e987a30696ba355920d6dcb3876f5&device_type=iPhone%205C&ssmix=a&aid=13&idfv=268E9FF9-A095-4656-B343-EB377C7CFA26&os_version=10.3.1&live_sdk_version=1.6.5&device_platform=iphone&ab_client=a1,f2,f7,e1&ac=WIFI&version_code=6.2.1&idfa=B69DF05F-7023-47D0-8AD0-D38943C67C75&ab_version=151249,150251,152612,153438,122834,143763,152346,144448,148160,151123,128825,153615,153256,152379,134128,153405,151918,151444,151723,152027,125174,144443,152435,152290,146839,136277,149047,151306,152060,153537,153234,151998,152955,122948,144237,31211,153070,150917,131207,145585,150352,151118&iid=12643423357&device_id=37581539214&LBS_status=authroize&category='+category+'&city=%E5%8C%97%E4%BA%AC&concern_id='+str(concern_id)+'&count=20&cp=519e769578AECq1&detail=1&image=1&language=zh-Hans-CN&last_refresh_sub_entrance_interval=4964&loc_mode=1&max_behot_time='+str(t)+'&refer=1&strict=0&tt_from=load_more'
head={
'Host'	:'lf.snssdk.com',
'Connection'	:'keep-alive',
'Cookie'	:'ba=BA0.2-20170512-51e32-fYF19EY05tqUazIdsQiZ; uid_tt=4e105bbd145c9beb07a123359b9fedd3; qh[360]=1; alert_coverage=90; login_flag=db35722bd823cde46bcdfe60f844adbd; sessionid=7edd6b18c34976f2d2612f82fa08d208; sid_tt=7edd6b18c34976f2d2612f82fa08d208; sid_guard="7edd6b18c34976f2d2612f82fa08d208|1501041443|2592000|Fri\054 25-Aug-2017 03:57:23 GMT"; install_id=12608887101; ttreq=1$d9fd07e95e195fccb3ecb718b6071a69f9cb382b; _ga=GA1.2.1897648744.1498908290; _gid=GA1.2.495535914.1501062435',
'Accept-Encoding'	:'gzip',
'User-Agent'	:'Dalvik/2.1.0 (Linux; U; Android 6.0.1; ZUK Z1 Build/MMB29M) NewsArticle/6.2.7 cronet/58.0.2991.0',
'X-SS-REQ-TICKET':	'1501063679513',
}

ret=requests.get(url1,headers=head,verify=False).content.decode(encoding='utf8')
x=json.loads(ret)
for item in x['data']:
    item['content']=json.loads(item['content'])

print(x)
