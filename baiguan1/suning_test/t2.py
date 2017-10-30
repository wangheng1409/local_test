#!user/bin/env python3
# -*- coding: utf8 -*-
import json
s='allBrandCallBack({"brandFilter":{"D":[{"value":"233555","valueDesc":"第一牛(DIYINIU)","valueCode":"5P41","checked":false,"appValueDesc":"","checkPic":true},{"value":"10116","valueDesc":"迪士尼(Disney)","valueCode":"2406","checked":false,"appValueDesc":"","checkPic":true},{"value":"40606","valueDesc":"第七公社(D7gongshe)","valueCode":"T349","checked":false,"appValueDesc":"","checkPic":true},{"value":"17901","valueDesc":"丹杰仕(DANJIESHI)","valueCode":"N300","checked":false,"appValueDesc":"","checkPic":true},{"value":"1331329","valueDesc":"朵维思(dowisi)","valueCode":"41D9","checked":false,"appValueDesc":"","checkPic":false},{"value":"2967605","valueDesc":"東材","valueCode":"55G0","checked":false,"appValueDesc":"","checkPic":false},{"value":"2397903","valueDesc":"DOUBLE CRAZY","valueCode":"49V5","checked":false,"appValueDesc":"","checkPic":false},{"value":"645670","valueDesc":"蒂妮佳(DInijia)","valueCode":"8F46","checked":false,"appValueDesc":"","checkPic":false},{"value":"915525","valueDesc":"朵维尔米(dower me)","valueCode":"121T","checked":false,"appValueDesc":"","checkPic":false},{"value":"2293243","valueDesc":"黛诗茹(Daishiru)","valueCode":"476R","checked":false,"appValueDesc":"","checkPic":false},{"value":"2227677","valueDesc":"迪鲁奥(DILUAO)","valueCode":"44S1","checked":false,"appValueDesc":"","checkPic":false}],"E":[{"value":"2993036","valueDesc":"ECTIC","valueCode":"562X","checked":false,"appValueDesc":"","checkPic":false},{"value":"2239468","valueDesc":"Eight Guys","valueCode":"454O","checked":false,"appValueDesc":"","checkPic":false},{"value":"645675","valueDesc":"espider","valueCode":"8F50","checked":false,"appValueDesc":"","checkPic":false}],"F":[{"value":"55676","valueDesc":"凡客诚品(VANCL)","valueCode":"B106","checked":false,"appValueDesc":"","checkPic":true},{"value":"242781","valueDesc":"梵希蔓(Vimly)","valueCode":"5X71","checked":false,"appValueDesc":"","checkPic":true},{"value":"10058","valueDesc":"范思哲(Versace)","valueCode":"0EGG","checked":false,"appValueDesc":"","checkPic":false},{"value":"2673257","valueDesc":"封后(FENGHOU)","valueCode":"53M1","checked":false,"appValueDesc":"","checkPic":false},{"value":"646214","valueDesc":"翡百裙(feibaiqun)","valueCode":"8K81","checked":false,"appValueDesc":"","checkPic":false},{"value":"2696932","valueDesc":"风沙渡","valueCode":"544L","checked":false,"appValueDesc":"","checkPic":false},{"value":"915135","valueDesc":"方氏·米希娅(FSMIXIYA)","valueCode":"116F","checked":false,"appValueDesc":"","checkPic":false},{"value":"2341267","valueDesc":"呋囡坊(FUNANFANG)","valueCode":"48I9","checked":false,"appValueDesc":"","checkPic":false},{"value":"2974833","valueDesc":"范西莱","valueCode":"55M1","checked":false,"appValueDesc":"","checkPic":false}],"G":[{"value":"651288","valueDesc":"歌诺瑞丝(GENUORUISI)","valueCode":"8W70","checked":false,"appValueDesc":"","checkPic":true},{"value":"16668","valueDesc":"古仕卡特(GUSSKATER)","valueCode":"N301","checked":false,"appValueDesc":"","checkPic":true},{"value":"255669","valueDesc":"古莱登(GODLIKE)","valueCode":"6L56","checked":false,"appValueDesc":"","checkPic":true},{"value":"990468","valueDesc":"戈思登","valueCode":"21A5","checked":false,"appValueDesc":"","checkPic":false},{"value":"1197964","valueDesc":"莞馨(wanxin)","valueCode":"32U9","checked":false,"appValueDesc":"","checkPic":false},{"value":"55555","valueDesc":"光迅","valueCode":"4222","checked":false,"appValueDesc":"","checkPic":false}],"A":[{"value":"42802","valueDesc":"安踏(ANTA)","valueCode":"6100","checked":false,"appValueDesc":"","checkPic":true},{"value":"19462","valueDesc":"阿玛尼(ARMANI)","valueCode":"0CPU","checked":false,"appValueDesc":"","checkPic":true},{"value":"914483","valueDesc":"艾凝雪(Ainingxue)","valueCode":"108V","checked":false,"appValueDesc":"","checkPic":true},{"value":"118550","valueDesc":"爱伊琪","valueCode":"1U89","checked":false,"appValueDesc":"","checkPic":true},{"value":"78425","valueDesc":"爱伊纳(eyyina)","valueCode":"1H87","checked":false,"appValueDesc":"","checkPic":true},{"value":"42048","valueDesc":"阿玛尼牛仔(Armani Jeans)","valueCode":"Y613","checked":false,"appValueDesc":"","checkPic":true},{"value":"262799","valueDesc":"艾诺利亚(AINOELIA)","valueCode":"7F40","checked":false,"appValueDesc":"","checkPic":true},{"value":"169471","valueDesc":"AR","valueCode":"2P61","checked":false,"appValueDesc":"","checkPic":true},{"value":"42667","valueDesc":"阿诗玛(Ashima)","valueCode":"R368","checked":false,"appValueDesc":"","checkPic":false},{"value":"953738","valueDesc":"艾芬俪(AIFENLI)","valueCode":"136F","checked":false,"appValueDesc":"","checkPic":false},{"value":"3047581","valueDesc":"岸森","valueCode":"571I","checked":false,"appValueDesc":"","checkPic":false},{"value":"2397956","valueDesc":"安娅诗","valueCode":"510R","checked":false,"appValueDesc":"","checkPic":false},{"value":"2341269","valueDesc":"爱拥者","valueCode":"48J1","checked":false,"appValueDesc":"","checkPic":false},{"value":"3045224","valueDesc":"安德玛踏","valueCode":"573Q","checked":false,"appValueDesc":"","checkPic":false}],"B":[{"value":"782201","valueDesc":"班俏(BANQIAO)","valueCode":"010I","checked":false,"appValueDesc":"","checkPic":true},{"value":"51319","valueDesc":"播","valueCode":"0V39","checked":false,"appValueDesc":"","checkPic":true},{"value":"118663","valueDesc":"倍佳斯","valueCode":"1W23","checked":false,"appValueDesc":"","checkPic":true},{"value":"10057","valueDesc":"博柏利(Burberry)","valueCode":"9331","checked":false,"appValueDesc":"","checkPic":true},{"value":"2257865","valueDesc":"BEARBURRY","valueCode":"462N","checked":false,"appValueDesc":"","checkPic":false},{"value":"3047127","valueDesc":"布尔根兰(BURGENLAND)","valueCode":"571A","checked":false,"appValueDesc":"","checkPic":false},{"value":"2341266","valueDesc":"百丽香奈(BAILIXIANGNAI)","valueCode":"48I8","checked":false,"appValueDesc":"","checkPic":false},{"value":"182709","valueDesc":"班瑞伊洛(Banreylo)","valueCode":"4H59","checked":false,"appValueDesc":"","checkPic":false},{"value":"228852","valueDesc":"贝瑞英格(BIRRYSHOP)","valueCode":"5L54","checked":false,"appValueDesc":"","checkPic":false},{"value":"2974298","valueDesc":"BOUSSAC","valueCode":"55N8","checked":false,"appValueDesc":"","checkPic":false},{"value":"2296859","valueDesc":"百魅兰蒂(BAIMEILANDI)","valueCode":"47C2","checked":false,"appValueDesc":"","checkPic":false},{"value":"2398482","valueDesc":"保骆威尔(Poll Verll)","valueCode":"50S5","checked":false,"appValueDesc":"","checkPic":false},{"value":"2341279","valueDesc":"步来褶惠","valueCode":"48K1","checked":false,"appValueDesc":"","checkPic":false},{"value":"2967814","valueDesc":"蓓嫣","valueCode":"55A7","checked":false,"appValueDesc":"","checkPic":false},{"value":"2638310","valueDesc":"宾如意","valueCode":"52X8","checked":false,"appValueDesc":"","checkPic":false}],"C":[{"value":"19998","valueDesc":"初语","valueCode":"S474","checked":false,"appValueDesc":"","checkPic":true},{"value":"131041","valueDesc":"ck","valueCode":"2O40","checked":false,"appValueDesc":"","checkPic":true},{"value":"1159887","valueDesc":"潮至(CHAOZHI)","valueCode":"29U5","checked":false,"appValueDesc":"","checkPic":true},{"value":"615675","valueDesc":"采轩(CAIXUAN)","valueCode":"8A95","checked":false,"appValueDesc":"","checkPic":true},{"value":"2968307","valueDesc":"CUM","valueCode":"55A0","checked":false,"appValueDesc":"","checkPic":false},{"value":"2699861","valueDesc":"创富晨(chuangfuchen)","valueCode":"546A","checked":false,"appValueDesc":"","checkPic":false},{"value":"2703983","valueDesc":"昌音雅","valueCode":"54B0","checked":false,"appValueDesc":"","checkPic":false},{"value":"118111","valueDesc":"C2潮朝(C2CHAOCHAO)","valueCode":"1M71","checked":false,"appValueDesc":"","checkPic":false},{"value":"2671894","valueDesc":"城市氛围(CTRLCITY)","valueCode":"53H8","checked":false,"appValueDesc":"","checkPic":false},{"value":"40207","valueDesc":"Calvin Klein","valueCode":"48X3","checked":false,"appValueDesc":"","checkPic":false}],"L":[{"value":"125916","valueDesc":"拉夏贝尔(La Chapelle)","valueCode":"2V88","checked":false,"appValueDesc":"","checkPic":true},{"value":"203180","valueDesc":"拉谷谷(Lagogo)","valueCode":"4Q81","checked":false,"appValueDesc":"","checkPic":true},{"value":"138771","valueDesc":"裂帛","valueCode":"8135","checked":false,"appValueDesc":"","checkPic":true},{"value":"1091300","valueDesc":"利科帕(LIKOPA)","valueCode":"24O2","checked":false,"appValueDesc":"","checkPic":true},{"value":"651229","valueDesc":"朗妮姿(LANGNIZI)","valueCode":"8W57","checked":false,"appValueDesc":"","checkPic":true},{"value":"43356","valueDesc":"李维斯(LEVI\u0027S)","valueCode":"6227","checked":false,"appValueDesc":"","checkPic":true},{"value":"981374","valueDesc":"Leioyda","valueCode":"17N7","checked":false,"appValueDesc":"","checkPic":true},{"value":"15957","valueDesc":"狼爪(Jack Wolfskin)","valueCode":"N128","checked":false,"appValueDesc":"","checkPic":true},{"value":"42935","valueDesc":"龙狮戴尔(LONSDALE)","valueCode":"Y069","checked":false,"appValueDesc":"","checkPic":true},{"value":"770698","valueDesc":"琳朵儿(LINDUOER)","valueCode":"9U70","checked":false,"appValueDesc":"","checkPic":true},{"value":"228867","valueDesc":"朗衣贝(Lang Yi Bei)","valueCode":"5L67","checked":false,"appValueDesc":"","checkPic":true},{"value":"14732","valueDesc":"裂帛鸟","valueCode":"M756","checked":false,"appValueDesc":"","checkPic":true},{"value":"645486","valueDesc":"伦敦雾","valueCode":"8C45","checked":false,"appValueDesc":"","checkPic":false},{"value":"2967512","valueDesc":"洛凌","valueCode":"55G3","checked":false,"appValueDesc":"","checkPic":false},{"value":"259025","valueDesc":"莉纳丝汀(LINASTIN)","valueCode":"6T64","checked":false,"appValueDesc":"","checkPic":false},{"value":"2922080","valueDesc":"黎多拉","valueCode":"552J","checked":false,"appValueDesc":"","checkPic":false},{"value":"2217252","valueDesc":"莱梦德(LAIMENGDE)","valueCode":"445I","checked":false,"appValueDesc":"","checkPic":false},{"value":"2993356","valueDesc":"黎拉图(LILATU)","valueCode":"563R","checked":false,"appValueDesc":"","checkPic":false},{"value":"1171340","valueDesc":"Liya\u0027s closet","valueCode":"305W","checked":false,"appValueDesc":"","checkPic":false},{"value":"172710","valueDesc":"拉尔夫·劳伦(RALPH LAUREN)","valueCode":"0CNU","checked":false,"appValueDesc":"","checkPic":false},{"value":"1297490","valueDesc":"凌之韵(LRYHME)","valueCode":"382Q","checked":false,"appValueDesc":"","checkPic":false},{"value":"2423917","valueDesc":"里若丝丽","valueCode":"529X","checked":false,"appValueDesc":"","checkPic":false},{"value":"2675717","valueDesc":"垒尚","valueCode":"53R5","checked":false,"appValueDesc":"","checkPic":false},{"value":"1344967","valueDesc":"Locoblue","valueCode":"432M","checked":false,"appValueDesc":"","checkPic":false}],"M":[{"value":"863404","valueDesc":"美特斯邦威(Meters/bonwe)","valueCode":"07H7","checked":false,"appValueDesc":"","checkPic":true},{"value":"215117","valueDesc":"M2monLine","valueCode":"P803","checked":false,"appValueDesc":"","checkPic":true},{"value":"1343065","valueDesc":"蜜维(MIWEI)","valueCode":"42A4","checked":false,"appValueDesc":"","checkPic":true},{"value":"1343645","valueDesc":"玛莲莎(MALIANSHA)","valueCode":"42U1","checked":false,"appValueDesc":"","checkPic":true},{"value":"1146417","valueDesc":"木每每(mumeimei)","valueCode":"284V","checked":false,"appValueDesc":"","checkPic":true},{"value":"2664563","valueDesc":"米斯魅","valueCode":"538X","checked":false,"appValueDesc":"","checkPic":false},{"value":"1245750","valueDesc":"慢跑者(MAN PAO ZHE)","valueCode":"34U7","checked":false,"appValueDesc":"","checkPic":false},{"value":"1294838","valueDesc":"铭浩依","valueCode":"37V1","checked":false,"appValueDesc":"","checkPic":false},{"value":"1341428","valueDesc":"默蒂梵(MODIFAN)","valueCode":"422R","checked":false,"appValueDesc":"","checkPic":false},{"value":"228216","valueDesc":"曼妮","valueCode":"5L38","checked":false,"appValueDesc":"","checkPic":false},{"value":"2989805","valueDesc":"梦珈轩","valueCode":"560G","checked":false,"appValueDesc":"","checkPic":false},{"value":"2724407","valueDesc":"MEZHBAG","valueCode":"54O6","checked":false,"appValueDesc":"","checkPic":false},{"value":"3068720","valueDesc":"密瓜森林","valueCode":"579X","checked":false,"appValueDesc":"","checkPic":false},{"value":"892005","valueDesc":"明地一族(ming di yi zhu)","valueCode":"08K9","checked":false,"appValueDesc":"","checkPic":false},{"value":"2993319","valueDesc":"迈尔尼诺(MYLE NINO)","valueCode":"563O","checked":false,"appValueDesc":"","checkPic":false},{"value":"1142495","valueDesc":"魅言魅语(MeiYanMeiYu)","valueCode":"27S0","checked":false,"appValueDesc":"","checkPic":false},{"value":"1310810","valueDesc":"沐晞","valueCode":"39B5","checked":false,"appValueDesc":"","checkPic":false},{"value":"989550","valueDesc":"魔灯诚堡(Muuduux)","valueCode":"19H2","checked":false,"appValueDesc":"","checkPic":false},{"value":"3049195","valueDesc":"牧兽","valueCode":"571F","checked":false,"appValueDesc":"","checkPic":false},{"value":"990531","valueDesc":"麦斯生活秀","valueCode":"21H8","checked":false,"appValueDesc":"","checkPic":false},{"value":"2308031","valueDesc":"萌感熊(MENGGANXIONG)","valueCode":"489L","checked":false,"appValueDesc":"","checkPic":false},{"value":"1302641","valueDesc":"玛思蓓丝","valueCode":"38O6","checked":false,"appValueDesc":"","checkPic":false},{"value":"2701226","valueDesc":"漫倪芳(Man Ni Fang)","valueCode":"548J","checked":false,"appValueDesc":"","checkPic":false},{"value":"2257856","valueDesc":"M.WOWL","valueCode":"462D","checked":false,"appValueDesc":"","checkPic":false}],"N":[{"value":"42403","valueDesc":"南极人(NanJiren)","valueCode":"0CMQ","checked":false,"appValueDesc":"","checkPic":true},{"value":"651041","valueDesc":"女先生(Mr female)","valueCode":"8W19","checked":false,"appValueDesc":"","checkPic":true},{"value":"2717376","valueDesc":"诺焕尔","valueCode":"54I4","checked":false,"appValueDesc":"","checkPic":false}],"O":[{"value":"823731","valueDesc":"ochirly","valueCode":"04T7","checked":false,"appValueDesc":"","checkPic":true},{"value":"242815","valueDesc":"OTHERMIX","valueCode":"5Y05","checked":false,"appValueDesc":"","checkPic":true},{"value":"991693","valueDesc":"欧凯茜(Aucassie)","valueCode":"23W8","checked":false,"appValueDesc":"","checkPic":true},{"value":"2402155","valueDesc":"OPZC","valueCode":"51H0","checked":false,"appValueDesc":"","checkPic":false},{"value":"1198651","valueDesc":"欧天娜","valueCode":"330F","checked":false,"appValueDesc":"","checkPic":false},{"value":"2924972","valueDesc":"讴帝(OD)","valueCode":"553Y","checked":false,"appValueDesc":"","checkPic":false},{"value":"863413","valueDesc":"欧芳佳(OUF ARNCCAA)","valueCode":"07I6","checked":false,"appValueDesc":"","checkPic":false}],"H":[{"value":"222401","valueDesc":"赫嫀(Hersheson)","valueCode":"4B91","checked":false,"appValueDesc":"","checkPic":true},{"value":"1094958","valueDesc":"郝啦","valueCode":"250D","checked":false,"appValueDesc":"","checkPic":true},{"value":"14040","valueDesc":"恒源祥","valueCode":"7384","checked":false,"appValueDesc":"","checkPic":true},{"value":"11448","valueDesc":"花花公子(PLAYBOY)","valueCode":"5533","checked":false,"appValueDesc":"","checkPic":true},{"value":"1265122","valueDesc":"汇采","valueCode":"367K","checked":false,"appValueDesc":"","checkPic":true},{"value":"61911","valueDesc":"韩都衣舍(HSTYLE)","valueCode":"0DHE","checked":false,"appValueDesc":"","checkPic":true},{"value":"1092763","valueDesc":"韩妃图(HANFEITU)","valueCode":"24W0","checked":false,"appValueDesc":"","checkPic":false},{"value":"2991821","valueDesc":"幻黛(HUANDAI)","valueCode":"560P","checked":false,"appValueDesc":"","checkPic":false},{"value":"2304342","valueDesc":"晗莉姿","valueCode":"47J6","checked":false,"appValueDesc":"","checkPic":false},{"value":"2672762","valueDesc":"haoduoyi","valueCode":"53O5","checked":false,"appValueDesc":"","checkPic":false},{"value":"649614","valueDesc":"徽派兄弟","valueCode":"8N58","checked":false,"appValueDesc":"","checkPic":false},{"value":"806344","valueDesc":"韩慕彩","valueCode":"032A","checked":false,"appValueDesc":"","checkPic":false},{"value":"211035","valueDesc":"红妮(Hongni)","valueCode":"2C56","checked":false,"appValueDesc":"","checkPic":false}],"I":[{"value":"2239482","valueDesc":"into the rainbow","valueCode":"455C","checked":false,"appValueDesc":"","checkPic":true},{"value":"2250404","valueDesc":"IYOGURT","valueCode":"45K0","checked":false,"appValueDesc":"","checkPic":false}],"J":[{"value":"990758","valueDesc":"娇诗朵(jiaoshido)","valueCode":"21Z3","checked":false,"appValueDesc":"","checkPic":true},{"value":"1179169","valueDesc":"锦满园","valueCode":"30R2","checked":false,"appValueDesc":"","checkPic":true},{"value":"11188","valueDesc":"吉普(Jeep)","valueCode":"0ATQ","checked":false,"appValueDesc":"","checkPic":true},{"value":"798755","valueDesc":"锦序(JINXU)","valueCode":"028M","checked":false,"appValueDesc":"","checkPic":true},{"value":"970131","valueDesc":"JACKFANES","valueCode":"14F6","checked":false,"appValueDesc":"","checkPic":false},{"value":"650750","valueDesc":"娇米诗(JIAOMISHI)","valueCode":"8U04","checked":false,"appValueDesc":"","checkPic":false},{"value":"915767","valueDesc":"爵拓(JUETUO)","valueCode":"12B2","checked":false,"appValueDesc":"","checkPic":false},{"value":"2698599","valueDesc":"JKVI\u0027S","valueCode":"545P","checked":false,"appValueDesc":"","checkPic":false},{"value":"1279168","valueDesc":"金仟億","valueCode":"36X5","checked":false,"appValueDesc":"","checkPic":false},{"value":"2398196","valueDesc":"杰瑞诗","valueCode":"49W7","checked":false,"appValueDesc":"","checkPic":false},{"value":"2993189","valueDesc":"纪尼诗(Jinishi)","valueCode":"563M","checked":false,"appValueDesc":"","checkPic":false},{"value":"2978944","valueDesc":"瑾汐(JINXI)","valueCode":"55L0","checked":false,"appValueDesc":"","checkPic":false},{"value":"240067","valueDesc":"槿秀禾衫","valueCode":"5X04","checked":false,"appValueDesc":"","checkPic":false},{"value":"263317","valueDesc":"锦铭七玥","valueCode":"7G04","checked":false,"appValueDesc":"","checkPic":false},{"value":"1332423","valueDesc":"简芷(JIANZHI)","valueCode":"41L7","checked":false,"appValueDesc":"","checkPic":false}],"K":[{"value":"1361473","valueDesc":"可莉允","valueCode":"43B9","checked":false,"appValueDesc":"","checkPic":true},{"value":"222673","valueDesc":"klaiba","valueCode":"4K23","checked":false,"appValueDesc":"","checkPic":false},{"value":"218278","valueDesc":"酷然(koraman)","valueCode":"Z092","checked":false,"appValueDesc":"","checkPic":false},{"value":"2815764","valueDesc":"珂依舍(Keyishe)","valueCode":"54R1","checked":false,"appValueDesc":"","checkPic":false},{"value":"1171295","valueDesc":"Kenzo","valueCode":"304B","checked":false,"appValueDesc":"","checkPic":false},{"value":"1175263","valueDesc":"Kruidvat","valueCode":"309V","checked":false,"appValueDesc":"","checkPic":false}],"U":[{"value":"219236","valueDesc":"UYUK","valueCode":"W978","checked":false,"appValueDesc":"","checkPic":false}],"T":[{"value":"42457","valueDesc":"特步(Xtep)","valueCode":"6102","checked":false,"appValueDesc":"","checkPic":true},{"value":"946058","valueDesc":"TCVV","valueCode":"12N9","checked":false,"appValueDesc":"","checkPic":true},{"value":"2663616","valueDesc":"TKY SHOP","valueCode":"539S","checked":false,"appValueDesc":"","checkPic":false},{"value":"2967304","valueDesc":"TURICUM","valueCode":"55A2","checked":false,"appValueDesc":"","checkPic":false},{"value":"264171","valueDesc":"拓谷(TUOGU)","valueCode":"7I04","checked":false,"appValueDesc":"","checkPic":false},{"value":"118230","valueDesc":"TOMMY HILFIGER","valueCode":"T987","checked":false,"appValueDesc":"","checkPic":false}],"W":[{"value":"645999","valueDesc":"舞天纱","valueCode":"8I62","checked":false,"appValueDesc":"","checkPic":true},{"value":"2398161","valueDesc":"维恩克","valueCode":"49B7","checked":false,"appValueDesc":"","checkPic":false},{"value":"2703757","valueDesc":"维喜黛(WEIXIDAI)","valueCode":"54C7","checked":false,"appValueDesc":"","checkPic":false},{"value":"990476","valueDesc":"无畏衣衣(WUWEIYIYI)","valueCode":"21B3","checked":false,"appValueDesc":"","checkPic":false},{"value":"911963","valueDesc":"唯帝歌","valueCode":"09X8","checked":false,"appValueDesc":"","checkPic":false},{"value":"1344858","valueDesc":"唯馨鸟","valueCode":"42V1","checked":false,"appValueDesc":"","checkPic":false},{"value":"915580","valueDesc":"维卡莱琳","valueCode":"122Z","checked":false,"appValueDesc":"","checkPic":false},{"value":"2555222","valueDesc":"薇侣(weilu)","valueCode":"52R3","checked":false,"appValueDesc":"","checkPic":false}],"V":[{"value":"251526","valueDesc":"VOA","valueCode":"6H15","checked":false,"appValueDesc":"","checkPic":true},{"value":"1357127","valueDesc":"VESiCE","valueCode":"434X","checked":false,"appValueDesc":"","checkPic":false},{"value":"2397892","valueDesc":"Vansop","valueCode":"508U","checked":false,"appValueDesc":"","checkPic":false},{"value":"1282049","valueDesc":"Vanled","valueCode":"372T","checked":false,"appValueDesc":"","checkPic":false}],"Q":[{"value":"770696","valueDesc":"情娇婷(QINGJIAOTING)","valueCode":"9U68","checked":false,"appValueDesc":"","checkPic":true},{"value":"223157","valueDesc":"樵","valueCode":"5D05","checked":false,"appValueDesc":"","checkPic":true},{"value":"130375","valueDesc":"其采","valueCode":"3G79","checked":false,"appValueDesc":"","checkPic":true},{"value":"1338481","valueDesc":"千仙仙","valueCode":"421Z","checked":false,"appValueDesc":"","checkPic":false},{"value":"789534","valueDesc":"骑士普丁(PUTINRIDER)","valueCode":"015D","checked":false,"appValueDesc":"","checkPic":false},{"value":"1206626","valueDesc":"情吻缘(Qingwenyuan)","valueCode":"338J","checked":false,"appValueDesc":"","checkPic":false},{"value":"2250382","valueDesc":"倾衣之家(qingyizhijia)","valueCode":"45H8","checked":false,"appValueDesc":"","checkPic":false},{"value":"1298442","valueDesc":"勤晴依恋(QINQINGYILIAN)","valueCode":"384D","checked":false,"appValueDesc":"","checkPic":false},{"value":"1312394","valueDesc":"七色群","valueCode":"39S3","checked":false,"appValueDesc":"","checkPic":false},{"value":"1137582","valueDesc":"千年虫(Qiannianchong)","valueCode":"279O","checked":false,"appValueDesc":"","checkPic":false}],"P":[{"value":"2443781","valueDesc":"娉语(PINGYU)","valueCode":"52H6","checked":false,"appValueDesc":"","checkPic":false},{"value":"991255","valueDesc":"Puella","valueCode":"226K","checked":false,"appValueDesc":"","checkPic":false},{"value":"2239480","valueDesc":"PREPPY ELITE","valueCode":"455A","checked":false,"appValueDesc":"","checkPic":false}],"S":[{"value":"1326400","valueDesc":"愫惠君(suhuijun)","valueCode":"418F","checked":false,"appValueDesc":"","checkPic":true},{"value":"190329","valueDesc":"苏醒的乐园","valueCode":"4K82","checked":false,"appValueDesc":"","checkPic":true},{"value":"132074","valueDesc":"声缎","valueCode":"3L59","checked":false,"appValueDesc":"","checkPic":true},{"value":"229241","valueDesc":"圣大保罗(SANTA BARBARA POLO \u0026 RACQUET CLUB)","valueCode":"8886","checked":false,"appValueDesc":"","checkPic":true},{"value":"1169736","valueDesc":"舒雅(Schiesser)","valueCode":"302G","checked":false,"appValueDesc":"","checkPic":false},{"value":"2407963","valueDesc":"珊诗丽","valueCode":"51O1","checked":false,"appValueDesc":"","checkPic":false},{"value":"915065","valueDesc":"斯妍","valueCode":"113L","checked":false,"appValueDesc":"","checkPic":false},{"value":"255224","valueDesc":"尚都比拉(SENTUBILA)","valueCode":"6K31","checked":false,"appValueDesc":"","checkPic":false},{"value":"650111","valueDesc":"Sait NOUVara","valueCode":"8P45","checked":false,"appValueDesc":"","checkPic":false},{"value":"990559","valueDesc":"莎密(SHAMI)","valueCode":"21L4","checked":false,"appValueDesc":"","checkPic":false},{"value":"3054419","valueDesc":"森马杰克","valueCode":"574X","checked":false,"appValueDesc":"","checkPic":false},{"value":"2339306","valueDesc":"思薇淑阁","valueCode":"48D8","checked":false,"appValueDesc":"","checkPic":false},{"value":"988861","valueDesc":"绅士空间(SENSIKJ)","valueCode":"185G","checked":false,"appValueDesc":"","checkPic":false},{"value":"2700112","valueDesc":"尚恩麦","valueCode":"545W","checked":false,"appValueDesc":"","checkPic":false},{"value":"1312684","valueDesc":"饰壹尚","valueCode":"39Y6","checked":false,"appValueDesc":"","checkPic":false},{"value":"2341268","valueDesc":"SSXOIW","valueCode":"48J0","checked":false,"appValueDesc":"","checkPic":false},{"value":"796790","valueDesc":"衫伊格(shanyige)","valueCode":"024W","checked":false,"appValueDesc":"","checkPic":false},{"value":"1139284","valueDesc":"SexeMara","valueCode":"27D4","checked":false,"appValueDesc":"","checkPic":false},{"value":"2682882","valueDesc":"四创","valueCode":"53Z2","checked":false,"appValueDesc":"","checkPic":false}],"R":[{"value":"234004","valueDesc":"RUILIBEIKA","valueCode":"5Q74","checked":false,"appValueDesc":"","checkPic":false},{"value":"991583","valueDesc":"然兹(ranzi)","valueCode":"23V5","checked":false,"appValueDesc":"","checkPic":false},{"value":"2994997","valueDesc":"苒曼丽(RAN MAN LI)","valueCode":"565S","checked":false,"appValueDesc":"","checkPic":false},{"value":"3012718","valueDesc":"芮图(RUI TU)","valueCode":"568G","checked":false,"appValueDesc":"","checkPic":false}],"Y":[{"value":"60775","valueDesc":"茵曼(INMAN)","valueCode":"A043","checked":false,"appValueDesc":"","checkPic":true},{"value":"40326","valueDesc":"妖精的口袋(ELFSACK)","valueCode":"T214","checked":false,"appValueDesc":"","checkPic":true},{"value":"915759","valueDesc":"烟花烫","valueCode":"12A9","checked":false,"appValueDesc":"","checkPic":true},{"value":"1146429","valueDesc":"与牧","valueCode":"285G","checked":false,"appValueDesc":"","checkPic":true},{"value":"236713","valueDesc":"忆香妃(YI XIANG FEI)","valueCode":"5T31","checked":false,"appValueDesc":"","checkPic":true},{"value":"796802","valueDesc":"依岚傲雪","valueCode":"025J","checked":false,"appValueDesc":"","checkPic":true},{"value":"978581","valueDesc":"蔚缇(Weiti)","valueCode":"15N1","checked":false,"appValueDesc":"","checkPic":true},{"value":"210802","valueDesc":"意宾(yibin)","valueCode":"1B30","checked":false,"appValueDesc":"","checkPic":true},{"value":"2279916","valueDesc":"邑概念","valueCode":"470Z","checked":false,"appValueDesc":"","checkPic":true},{"value":"55425","valueDesc":"依尼(ELLE)","valueCode":"B594","checked":false,"appValueDesc":"","checkPic":false},{"value":"1144689","valueDesc":"逸阳","valueCode":"281F","checked":false,"appValueDesc":"","checkPic":false},{"value":"915064","valueDesc":"优艾丝(UAISI)","valueCode":"113K","checked":false,"appValueDesc":"","checkPic":false},{"value":"42228","valueDesc":"雨果博斯(HUGO BOSS)","valueCode":"0ELD","checked":false,"appValueDesc":"","checkPic":false},{"value":"956359","valueDesc":"余果贝尔(YoungBell)","valueCode":"139W","checked":false,"appValueDesc":"","checkPic":false},{"value":"20512","valueDesc":"伊花裳语","valueCode":"V424","checked":false,"appValueDesc":"","checkPic":false},{"value":"2352368","valueDesc":"娅克魅(YAKEMEI)","valueCode":"497D","checked":false,"appValueDesc":"","checkPic":false},{"value":"1094980","valueDesc":"依伶梦(.)","valueCode":"251A","checked":false,"appValueDesc":"","checkPic":false}],"X":[{"value":"266282","valueDesc":"纤莉秀(qianlixiu)","valueCode":"7M92","checked":false,"appValueDesc":"","checkPic":true},{"value":"914611","valueDesc":"新颖阿玛施正(NOVEL AMASS ZEN)","valueCode":"109Y","checked":false,"appValueDesc":"","checkPic":true},{"value":"261846","valueDesc":"绣娘","valueCode":"6Z19","checked":false,"appValueDesc":"","checkPic":true},{"value":"41887","valueDesc":"秀族(XIUZU)","valueCode":"N028","checked":false,"appValueDesc":"","checkPic":true},{"value":"651706","valueDesc":"香港聖芬婷(HONG KONG SHENGFENTING)","valueCode":"8Z69","checked":false,"appValueDesc":"","checkPic":true},{"value":"255671","valueDesc":"熙世界(sllsky)","valueCode":"6L58","checked":false,"appValueDesc":"","checkPic":true},{"value":"42422","valueDesc":"雪中飞(SNOW FLYING)","valueCode":"A888","checked":false,"appValueDesc":"","checkPic":true},{"value":"2398146","valueDesc":"修娴(soossn)","valueCode":"504B","checked":false,"appValueDesc":"","checkPic":false},{"value":"1147911","valueDesc":"新奇鼠(novelmice)","valueCode":"28A7","checked":false,"appValueDesc":"","checkPic":false},{"value":"233997","valueDesc":"溪谷花开","valueCode":"5Q67","checked":false,"appValueDesc":"","checkPic":false},{"value":"1300581","valueDesc":"小魔鱼","valueCode":"389S","checked":false,"appValueDesc":"","checkPic":false},{"value":"2978897","valueDesc":"雪魅尔(XUEMEIER)","valueCode":"55L3","checked":false,"appValueDesc":"","checkPic":false},{"value":"651756","valueDesc":"徐健","valueCode":"9A21","checked":false,"appValueDesc":"","checkPic":false},{"value":"1246670","valueDesc":"贤淑女郎(xianshunvlang)","valueCode":"34V5","checked":false,"appValueDesc":"","checkPic":false},{"value":"118927","valueDesc":"炫出自我(XUANCHUZIWO)","valueCode":"1M79","checked":false,"appValueDesc":"","checkPic":false},{"value":"2261192","valueDesc":"纤衣楚楚","valueCode":"468U","checked":false,"appValueDesc":"","checkPic":false},{"value":"1189469","valueDesc":"仙卡婷(XianKaTing)","valueCode":"327F","checked":false,"appValueDesc":"","checkPic":false}],"Z":[{"value":"915685","valueDesc":"ZARA KARA","valueCode":"127H","checked":false,"appValueDesc":"","checkPic":true},{"value":"236533","valueDesc":"佐露絲(RALOS)","valueCode":"5S21","checked":false,"appValueDesc":"","checkPic":true},{"value":"190302","valueDesc":"尊首(ZUNSHOU)","valueCode":"4P77","checked":false,"appValueDesc":"","checkPic":true},{"value":"650401","valueDesc":"芷臻(zhizhen)","valueCode":"8S04","checked":false,"appValueDesc":"","checkPic":true},{"value":"262802","valueDesc":"臻依缘","valueCode":"7F43","checked":false,"appValueDesc":"","checkPic":true},{"value":"2347552","valueDesc":"ZARP","valueCode":"491C","checked":false,"appValueDesc":"","checkPic":false},{"value":"229244","valueDesc":"卓多姿(Z\u0027DORZI)","valueCode":"5L74","checked":false,"appValueDesc":"","checkPic":false},{"value":"2685434","valueDesc":"泽美夕(ZEMEIXI)","valueCode":"53Y6","checked":false,"appValueDesc":"","checkPic":false},{"value":"1294840","valueDesc":"子沫雨(JMOORY)","valueCode":"37V3","checked":false,"appValueDesc":"","checkPic":false},{"value":"1237935","valueDesc":"珍真羊(Zhenzhenyang)","valueCode":"34O0","checked":false,"appValueDesc":"","checkPic":false},{"value":"1159342","valueDesc":"卓勝基","valueCode":"29R1","checked":false,"appValueDesc":"","checkPic":false},{"value":"1226510","valueDesc":"卓云山峰","valueCode":"34G8","checked":false,"appValueDesc":"","checkPic":false}],"#":[{"value":"2277673","valueDesc":"美莎帕(mesappas)","valueCode":"46U9","checked":false,"appValueDesc":"","checkPic":true},{"value":"3041242","valueDesc":"形象茗模","valueCode":"570W","checked":false,"appValueDesc":"","checkPic":false},{"value":"3023850","valueDesc":"抹卡","valueCode":"56K7","checked":false,"appValueDesc":"","checkPic":false},{"value":"953741","valueDesc":"大足龙(DAZULONG)","valueCode":"136I","checked":false,"appValueDesc":"","checkPic":false},{"value":"2398022","valueDesc":"百素","valueCode":"50R4","checked":false,"appValueDesc":"","checkPic":false},{"value":"2982017","valueDesc":"漂亮百合(Piaoliangbaihe)","valueCode":"55T8","checked":false,"appValueDesc":"","checkPic":false},{"value":"2960825","valueDesc":"绰娅","valueCode":"555Q","checked":false,"appValueDesc":"","checkPic":false},{"value":"2698023","valueDesc":"派尼美特","valueCode":"545T","checked":false,"appValueDesc":"","checkPic":false},{"value":"2398179","valueDesc":"纤曼悠(QIANMANYOU)","valueCode":"499N","checked":false,"appValueDesc":"","checkPic":false},{"value":"3032505","valueDesc":"莱依得美","valueCode":"56O4","checked":false,"appValueDesc":"","checkPic":false},{"value":"2998436","valueDesc":"信仰者","valueCode":"567D","checked":false,"appValueDesc":"","checkPic":false},{"value":"3055585","valueDesc":"谜局(MIJU)","valueCode":"576Z","checked":false,"appValueDesc":"","checkPic":false},{"value":"3093954","valueDesc":"觅橙(FINDORANGE)","valueCode":"57X1","checked":false,"appValueDesc":"","checkPic":false},{"value":"2847732","valueDesc":"雅馨季","valueCode":"551P","checked":false,"appValueDesc":"","checkPic":false},{"value":"3030251","valueDesc":"艾尚恋族","valueCode":"56L0","checked":false,"appValueDesc":"","checkPic":false},{"value":"2984245","valueDesc":"婔垛坊(FEIDUOFANG)","valueCode":"55V3","checked":false,"appValueDesc":"","checkPic":false},{"value":"2639341","valueDesc":"碧沁伊人","valueCode":"530F","checked":false,"appValueDesc":"","checkPic":false},{"value":"2693869","valueDesc":"芝顿","valueCode":"541K","checked":false,"appValueDesc":"","checkPic":false},{"value":"2955279","valueDesc":"芸阁纤坊","valueCode":"554X","checked":false,"appValueDesc":"","checkPic":false},{"value":"2984161","valueDesc":"榄将(LANJIANG)","valueCode":"55Q1","checked":false,"appValueDesc":"","checkPic":false},{"value":"2662172","valueDesc":"秋壳","valueCode":"536W","checked":false,"appValueDesc":"","checkPic":false},{"value":"2398772","valueDesc":"阿妮萱(A.ni.xuan)","valueCode":"512Z","checked":false,"appValueDesc":"","checkPic":false},{"value":"2411152","valueDesc":"薮雀","valueCode":"51S2","checked":false,"appValueDesc":"","checkPic":false},{"value":"3047085","valueDesc":"麦瑞思(MAR PAIRS)","valueCode":"573G","checked":false,"appValueDesc":"","checkPic":false},{"value":"2994678","valueDesc":"派衣閣(PAIYIGE)","valueCode":"564J","checked":false,"appValueDesc":"","checkPic":false}]},"debugQuery":{}});'

left = s.index('{')
tmp = s[left:].strip()[:-2].replace(' ', '').replace('"}"', '""').replace('\\', '') \
    .replace('{"', '#@1').replace('":"', '#@2').replace('":', '#@3').replace('","', '#@4') \
    .replace(',"', '#@5').replace('"}', '#@6').replace('["', '#@7').replace('"]', '#@8') \
    .replace('"', '') \
    .replace('#@1', '{"').replace('#@2', '":"').replace('#@3', '":').replace('#@4', '","') \
    .replace('#@5', ',"').replace('#@6', '"}').replace('#@7', '["').replace('#@8', '"]')
try:
    goods_dic = json.loads(tmp)
except Exception as e:
    print(e)
    print(tmp)


brandFilter=goods_dic['brandFilter']
new_brand_list=[]
for k,brand_item in brandFilter.items():
    if k=='#':
        continue
    else:
        new_brand_list.append([v['value'] for v in brand_item if v['value']])

brand_list=[x for y in new_brand_list for x in y]

print(brand_list)