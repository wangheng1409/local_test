import requests
import json

url='https://lf.snssdk.com/article/category/get_subscribed/v2/?iid=12608887101&device_id=11261174909&ac=wifi&channel=update&aid=13&app_name=news_article&version_code=627&version_name=6.2.7&device_platform=android&ab_version=152337%2C145535%2C145531%2C150251%2C152151%2C153439%2C152351%2C152367%2C122834%2C143763%2C144447%2C148160%2C149168%2C151125%2C144592%2C146015%2C134128%2C153409%2C151447%2C151726%2C152026%2C125174%2C144444%2C153005%2C147122%2C152436%2C152290%2C146839%2C149048%2C151308%2C145888%2C152060%2C150951%2C122948%2C31642%2C148564%2C131207%2C153403%2C145585%2C152731%2C150352%2C151116&ab_client=a1%2Cc4%2Ce1%2Cf2%2Cg2%2Cf7&ab_feature=102749%2C94563&abflag=3&ssmix=a&device_type=ZUK+Z1&device_brand=ZUK&language=zh&os_api=23&os_version=6.0.1&uuid=867695021907281&openudid=61c033e4371dc3f5&manifest_version_code=627&resolution=1080*1920&dpi=480&update_version_code=6275&_rticket=1501062924643'
header={
'Host'	:'lf.snssdk.com',
'Connection'	:'keep-alive',
'Cookie':'ba=BA0.2-20170512-51e32-fYF19EY05tqUazIdsQiZ; uid_tt=4e105bbd145c9beb07a123359b9fedd3; qh[360]=1; alert_coverage=90; login_flag=db35722bd823cde46bcdfe60f844adbd; sessionid=7edd6b18c34976f2d2612f82fa08d208; sid_tt=7edd6b18c34976f2d2612f82fa08d208; sid_guard="7edd6b18c34976f2d2612f82fa08d208|1501041443|2592000|Fri\054 25-Aug-2017 03:57:23 GMT"; install_id=12608887101; ttreq=1$d9fd07e95e195fccb3ecb718b6071a69f9cb382b; _ga=GA1.2.1897648744.1498908290; _gid=GA1.2.495535914.1501062435',
'Accept-Encoding'	:'gzip',
'User-Agent'	:'Dalvik/2.1.0 (Linux; U; Android 6.0.1; ZUK Z1 Build/MMB29M) NewsArticle/6.2.7 cronet/58.0.2991.0',
'X-SS-REQ-TICKET':	'1501063679280',
'Content-Type'	:'application/x-www-form-urlencoded; charset=UTF-8',
}

data={
    'city'	:'北京市',
    'latitude'	:'39.947205',
    'longitude'	 :'116.412967',
    'loc_time'  :	'1501041270',
    'categories'	:'["__all__","subscription","news_society","stock","news_local","video","news_sports","news_hot","question_and_answer",'
                     '"news_tech","news_car","news_finance","news_military","news_world","essay_joke","image_funny","image_ppmm","news_health","funny",'
                     '"news_house","news_history","news_regimen","digital","cellphone","宠物","news_culture","news_collect","boutique","science_all","news_comic","中国好表演",'
                     '"essay_saying","news_astrology","彩票","pregnancy","news_baby","positive","jinritemai","组图","live_talk","news_fashion","news_food","news_travel","emotion",'
                     '"movie","news_entertainment","news_agriculture","news_story","novel_channel","rumor","news_edu","news_home","government","image_wonderful","中国新唱将","news_game","快乐男声","hotsoon"]',
    'version'	:'11261174909|14|1501062886',
    'user_modify'	:'1',
    'iid'	:'12608887101',
    'device_id'	:'11261174909',
    'ac':	'wifi',
    'channel':	'update',
    'aid'	:'13',
    'app_name'	:'news_article',
    'version_code':	'627',
    'version_name':	'6.2.7',
    'device_platform':	'android',
    'ab_version':	'152337,145535,145531,150251,152151,153439,152351,152367,122834,143763,144447,148160,149168,151125,144592,146015,134128,153409,151447,151726,152026,125174,144444,153005,147122,152436,152290,146839,149048,151308,145888,152060,150951,122948,31642,148564,131207,153403,145585,152731,150352,151116',
    'ab_client'	:'a1,c4,e1,f2,g2,f7',
    'ab_feature':	'102749,94563',
    'abflag'	:'3',
    'ssmix':	'a',
    'device_type':	'ZUK Z1',
    'device_brand':	'ZUK',
    'language'	:'zh',
    'os_api'	:'23',
    'os_version'	:'6.0.1',
    'uuid'	:'867695021907281',
    'openudid'	:'61c033e4371dc3f5',
    'manifest_version_code':	'627',
    'resolution'	:'1080*1920',
    'dpi'	:'480',
    'update_version_code'	:'6275',
    '_rticket'	:'1501062924629',

}
ret=requests.post(url=url,data=data,verify=False,headers=header)
rs=json.loads(ret.text)['data']['data']
print(len(rs),rs)



