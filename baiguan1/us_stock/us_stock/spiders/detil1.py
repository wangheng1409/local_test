# -*- coding: utf-8 -*-
import scrapy
import json
import datetime
import time
import redis
from scrapy_redis.spiders import RedisSpider
from scrapy.conf import settings
from us_stock.items import UsStockItem
from us_stock.before.before import headers

BASE_URL='https://whalewisdom.com/stock/'
company_list=['twou', 'jobs', 'abmd', 'achc', 'acad', 'aciw', 'acxm', 'aeis', 'agio', 'agnc', 'agncb', 'akam', 'akrx',
              'alks', 'algt', 'mdrx', 'alny', 'aya', 'amcx', 'dox', 'amed', 'uhal', 'anat', 'amkr', 'afsi', 'arcc',
              'arrs', 'azpn', 'athn', 'aby', 'team', 'avxs', 'bcpc', 'ozrk', 'becn', 'bbby', 'bgcp', 'tech', 'bivv',
              'blkb', 'bbry', 'hawk', 'blmn', 'buff', 'blue', 'bokf', 'brcd', 'brkr', 'bwld', 'chrw', 'cdns', 'cacq',
              'cbf', 'cffn', 'casy', 'caty', 'cavm', 'cdk', 'cdw', 'cdev', 'cyou', 'chfc', 'cbpo', 'htht', 'chdn', 'cmpr',
              'crus', 'clvs', 'coke', 'cgnx', 'cohr', 'colb', 'colm', 'cbsh', 'cbshp', 'comm', 'cvlt', 'cprt', 'csod', 'csgp',
              'cbrl', 'cacc', 'cree', 'crto', 'cvbf', 'cy', 'cone', 'play', 'dxcm', 'fang', 'disck', 'dorm', 'dnkn', 'egbn',
              'ewbc', 'sats', 'eslt', 'efii', 'endp', 'esgr', 'entg', 'erie', 'eeft', 'exas', 'exel', 'xog', 'ffiv', 'fgen',
              'fngn', 'fnsr', 'feye', 'fcfs', 'fcnca', 'ffin', 'fhb', 'fibk', 'fmbi', 'fslr', 'fv', 'qtec', 'fsv', 'five',
              'flex', 'flir', 'ftnt', 'fult', 'glpg', 'glpi', 'grmn', 'gntx', 'gbci', 'glng', 'lope', 'omab', 'ggal', 'gpor',
              'gwph', 'hbhc', 'ha', 'hds', 'hcsg', 'hqy', 'hele', 'homb', 'hope', 'hpt', 'twnk', 'hcm', 'iac', 'ibkc', 'iep',
              'iclr', 'icui', 'iivi', 'ilg', 'incr', 'podd', 'iart', 'idti', 'icpt', 'idcc', 'iboc', 'isbc', 'ions', 'ipgp',
              'irbt', 'irwd', 'tlt', 'ixus', 'acwx', 'acwi', 'aaxj', 'mchi', 'scz', 'ibb', 'itri', 'jjsf', 'jbht', 'jcom', 'jkhy',
              'jack', 'jazz', 'jblu', 'juno', 'kite', 'klxi', 'lamr', 'lanc', 'lstr', 'laur', 'lexea', 'lexeb', 'lila', 'lilak',
              'lvnta', 'lvntb', 'fwonk', 'lpnt', 'lgnd', 'leco', 'lfus', 'livn', 'logi', 'logm', 'lpla', 'lulu', 'lite', 'mtsi',
              'manh', 'mktx', 'mrvl', 'masi', 'mtch', 'mat', 'matw', 'mbfi', 'mdso', 'mlnx', 'meoh', 'mgee', 'mscc', 'mstr', 'mksi',
              'momo', 'mpwr', 'morn', 'msg', 'fizz', 'nghc', 'nati', 'navi', 'nktr', 'neog', 'ntct', 'nbix', 'nws', 'nwsa', 'nxst',
              'nice', 'ndsn', 'nuan', 'ntnx', 'nuva', 'odp', 'okta', 'odfl', 'onb', 'olli', 'on', 'otex', 'opk', 'pacw', 'paas',
              'pnra', 'pzza', 'prxl', 'pegi', 'pdco', 'pten', 'pcty', 'pdce', 'pega', 'pbct', 'ppc', 'pnfp', 'pool', 'bpop', 'ptla',
              'prah', 'psmt', 'pvtb', 'pfpt', 'psec', 'prta', 'ptc', 'pbyi', 'qgen', 'qrvo', 'gold', 'roll', 'rp', 'rrr', 'roic',
              'rgld', 'sabr', 'sage', 'safm', 'sanm', 'sgms', 'sni', 'sgen', 'seic', 'sir', 'sigi', 'smtc', 'snh', 'sbny', 'slgn',
              'slab', 'spil', 'sina', 'sbgi', 'slm', 'lnce', 'ssb', 'save', 'splk', 'sfm', 'ssnc', 'stmp', 'spls', 'stld', 'srcl',
              'shoo', 'sivb', 'ttwo', 'tecd', 'tell', 'tsro', 'ttek', 'tcbi', 'txrh', 'tfsl', 'abco', 'cg', 'cake', 'gt', 'hain',
              'mdco', 'mik', 'midd', 'ttd', 'ulti', 'tbph', 'tivo', 'tsem', 'tsco', 'trmb', 'trip', 'trvg', 'trmk', 'ubnt', 'upl',
              'rare', 'umbf', 'umpq', 'ubsi', 'unfi', 'uthr', 'unit', 'oled', 'urbn', 'vnqi', 'vmbs', 'vtip', 'bndx', 'vxus', 'woof',
              'veon', 'vrnt', 'vrsn', 'vsat', 'viav', 'csa', 'virt', 'vwr', 'wafd', 'wbmd', 'wen', 'wern', 'wins', 'wtfc', 'wix', 'wwd',
              'wmgi', 'yndx', 'yerr', 'yy', 'zbra', 'z', 'zg', 'zion', 'znga']
company_list2=['ddd', 'wuba', 'aan', 'abm', 'akr', 'ayi', 'adnt', 'atge', 'aap', 'adsw', 'acm', 'aer', 'amg', 'agco', 'al', 'aks',
               'agi', 'aa', 'alr', 'alex', 'alx', 'aqn', 'y', 'alle', 'ale', 'ab', 'lnt', 'awh', 'alsn', 'ally', 'ach', 'amc',
               'amfw', 'acc', 'aeo', 'ael', 'afg', 'amh', 'apu', 'au', 'axe', 'amgp', 'am', 'ar', 'aiv', 'aple', 'ait', 'atr',
               'wtr', 'armk', 'ard', 'ares', 'awi', 'arw', 'apam', 'ash', 'ahl', 'asb', 'aiz', 'ago', 'af', 'ato', 'auo', 'athm',
               'alv', 'an', 'avy', 'ava', 'avt', 'avx', 'axta', 'axs', 'axon', 'azul', 'bgs', 'bxs', 'boh', 'bku', 'b', 'bfr',
               'bdc', 'bms', 'bery', 'big', 'bio', 'bkh', 'bkfs', 'bsm', 'bwp', 'bah', 'bwa', 'box', 'byd', 'bdn', 'bak', 'brfs',
               'bfam', 'bco', 'brx', 'br', 'bkd', 'bpy', 'bep', 'bro', 'bc', 'bpl', 'bvn', 'burl', 'bwxt', 'cj', 'cab', 'cabo',
               'cbt', 'caci', 'cae', 'caa', 'cpe', 'cpn', 'cpt', 'ccj', 'cwh', 'cmd', 'bxmt', 'ccp', 'csl', 'cri', 'ctlt', 'fun',
               'cx', 'cnco', 'ebr', 'cf', 'crl', 'che', 'cc', 'chk', 'cim', 'cea', 'znh', 'chh', 'cien', 'xec', 'cnk', 'cit',
               'clh', 'cldr', 'cno', 'utf', 'cfx', 'clns', 'sfr', 'cxp', 'cmc', 'cbu', 'cig', 'cbd', 'sbs', 'elp', 'ccu', 'cmp',
               'cndt', 'cnx', 'cvg', 'cpa', 'clb', 'cxw', 'clgx', 'cor', 'ofc', 'cotv', 'cot', 'cuz', 'cpl', 'cr', 'cpg', 'cck',
               'csra', 'cst', 'cube', 'cfr', 'cw', 'dan', 'dar', 'dcp', 'dct', 'ddr', 'deck', 'dlx', 'drh', 'dks', 'dbd', 'dlb',
               'dm', 'ufs', 'dci', 'dsl', 'dei', 'rdy', 'drq', 'dst', 'dnp', 'dnb', 'dft', 'dy', 'exp', 'egp', 'ev', 'exg', 'edr',
               'ee', 'ego', 'elli', 'erj', 'eme', 'esrt', 'enbl', 'eep', 'eca', 'enic', 'eocc', 'egn', 'enr', 'epc', 'erf', 'ens',
               'enlk', 'enlc', 'evhc', 'epam', 'epr', 'eqgp', 'eqm', 'eqc', 'els', 'esnt', 'esl', 'evr', 'stay', 'exr', 'fnb',
               'fds', 'fico', 'fcb', 'frt', 'fii', 'fbr', 'fnfv', 'faf', 'fcfs', 'fhn', 'fr', 'fnd', 'flo', 'fls', 'flr', 'fl',
               'fig', 'fbhs', 'fdp', 'fsic', 'gme', 'gps', 'gdi', 'gatx', 'gcp', 'gnrc', 'gwr', 'gel', 'g', 'geo', 'ggb', 'gil',
               'gmed', 'gddy', 'gol', 'gfi', 'ggg', 'ghc', 'gpt', 'gpk', 'gxp', 'gwb', 'gef', 'grub', 'pac', 'asr', 'aval', 'gsh',
               'gwre', 'hrb', 'ful', 'hae', 'hbi', 'hog', 'he', 'hr', 'hta', 'hls', 'hl', 'hei', 'hp', 'hlf', 'hxl', 'hiw', 'hi',
               'hrc', 'hth', 'hgv', 'hep', 'hfc', 'hli', 'hhc', 'hrg', 'hubb', 'hubs', 'hpp', 'hii', 'hun', 'h', 'iag', 'ida',
               'iex', 'iba', 'ngvt', 'ingr', 'igt', 'ipg', 'inxn', 'xon', 'invh', 'irm', 'icl', 'itcb', 'itt', 'jbl', 'jec', 'jag',
               'jhx', 'jeld', 'jbt', 'jll', 'ks', 'kar', 'kate', 'kyn', 'kbr', 'kmpr', 'kmt', 'kw', 'keys', 'krc', 'kim', 'kgc',
               'kex', 'kkr', 'knx', 'kss', 'kos', 'kro', 'kt', 'lw', 'lpi', 'lho', 'ltm', 'laz', 'lcii', 'lm', 'leg', 'ldos', 'lc',
               'lii', 'luk', 'lxp', 'lpt', 'lsi', 'ln', 'lad', 'lyv', 'lpx', 'lxft', 'mac', 'cli', 'mic', 'bma', 'm', 'main', 'mnk',
               'manu', 'man', 'vac', 'door', 'mtz', 'mtdr', 'mms', 'mdu', 'mpw', 'md', 'mcy', 'mdp', 'mfa', 'mtg', 'kors', 'mtx',
               'mbt', 'moh', 'mos', 'msa', 'msm', 'msci', 'msg', 'mule', 'mur', 'musa', 'nbr', 'nfg', 'nhi', 'nnn', 'sid', 'nav',
               'ncr', 'nvro', 'newr', 'nrz', 'nycb', 'nyt', 'nfx', 'njr', 'neu', 'ni', 'nomd', 'osb', 'nord', 'jwn', 'ntl', 'nwe',
               'nrg', 'nyld', 'nus', 'ns', 'nvg', 'nuv', 'nea', 'nac', 'nzf', 'nad', 'jps', 'nvr', 'oak', 'oas', 'oii', 'oge',
               'ori', 'oln', 'ohi', 'asgn', 'ogs', 'omf', 'oa', 'ora', 'osk', 'out', 'oc', 'oi', 'pkg', 'pam', 'pgre', 'pk', 'pe',
               'pthn', 'payc', 'pbf', 'btu', 'pso', 'peb', 'pag', 'pen', 'pfgc', 'pki', 'pze', 'psxp', 'doc', 'pdm', 'pci', 'pf',
               'pnw', 'pbi', 'pagp', 'plnt', 'pah', 'phi', 'pnm', 'pii', 'pol', 'por', 'post', 'pbh', 'pri', 'pra', 'pb', 'psb',
               'phm', 'pstg', 'pvh', 'qep', 'qts', 'pwr', 'ctx', 'rdn', 'rl', 'rrc', 'ryn', 'rlgy', 'rbc', 'rgc', 'rga', 'rs',
               'rnr', 'rpai', 'rxn', 'rice', 'rmp', 'rng', 'rba', 'rad', 'rli', 'rlj', 'rhi', 'rol', 'res', 'rpm', 'rspp', 'r',
               'rhp', 'sbh', 'sc', 'scg', 'sndr', 'saic', 'smg', 'see', 'smi', 'st', 'sxt', 'srg', 'sci', 'serv', 'shlx', 'shop',
               'sig', 'ssd', 'shi', 'six', 'skx', 'sm', 'aos', 'sna', 'sqm', 'son', 'bid', 'sji', 'swx', 'swn', 'spb', 'sr', 'spr',
               'src', 'sq', 'stag', 'stn', 'stwd', 'scs', 'scl', 'ste', 'stl', 'sf', 'stor', 'sum', 'sui', 'sun', 'sho', 'swft',
               'snx', 'snv', 'data', 'taho', 'tal', 'tegp', 'tep', 'skt', 'trgp', 'taro', 'tco', 'tmhc', 'tcp', 'tcf', 'tgna',
               'teo', 'tdy', 'tfx', 'tds', 'tpx', 'ten', 'tdc', 'ter', 'tex', 'tx', 'tllp', 'tpl', 'aes', 'thg', 'tho', 'tsu',
               'tkr', 'tol', 'tmk', 'ttc', 'rig', 'tgs', 'tru', 'ths', 'trco', 'tnet', 'trn', 'tse', 'tup', 'tkc', 'trq', 'twlo',
               'two', 'tyl', 'slca', 'ugi', 'ua', 'unf', 'umc', 'uri', 'usm', 'x', 'unvr', 'ue', 'usfd', 'usg', 'mtn', 'vrx', 'vlp',
               'vr', 'vly', 'vmi', 'vvv', 'var', 'vgr', 'vvc', 'veev', 'ver', 'pay', 'vet', 'vsm', 'vips', 'vsh', 'vc', 'vst',
               'voya', 'wpc', 'wrb', 'gra', 'wbc', 'wage', 'wre', 'wso', 'wts', 'w', 'wft', 'wbs', 'wri', 'wbt', 'wcg', 'wcc',
               'wst', 'wr', 'wal', 'wgp', 'wes', 'wu', 'wab', 'wlk', 'wex', 'wgl', 'wpm', 'wtm', 'wll', 'wsm', 'www', 'int', 'wor',
               'wpx', 'xhr', 'xrx', 'xpo', 'xyl', 'auy', 'yelp', 'ypf', 'zayo', 'zen']


class StockSpider(RedisSpider):
    name = "stockspider1"
    allowed_domains = []
    redis_key = 'stockspider1'
    if not settings['TEST']:
        pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db='0', password='bigone2016')
    else:
        pool = redis.ConnectionPool(host='127.0.0.1', port='6379', db='0')
    r = redis.Redis(connection_pool=pool)

    def start_requests(self):
        for company in company_list2:
            url=BASE_URL+company
            header={
                'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'accept-encoding':'gzip, deflate, br',
                'accept-language':'zh-CN,zh;q=0.8',
                'cache-control':'max-age=0',
                'if-none-match':'W/"ff142815283d32c734a9b772251e9b82"',
                'upgrade-insecure-requests':'1',
                'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36'
            }
            yield scrapy.Request(url, method="GET",headers=header,
                                  callback=self.parse0,
                                  dont_filter=True,
                                  meta={'name': company,
                                        }
                                  )
    def parse0(self,response):
        name = response.meta['name']
        ret=response.text
        item_id=ret.split('stock_id=')[1].split(';')[0]
        url, header = headers(item_id, 1)
        yield scrapy.Request(url, method="GET", headers=header,
                             callback=self.parse,
                             dont_filter=True,
                             meta={'name': name,
                                   'item_id': item_id,
                                   'page': 1,
                                   }
                             )


    def parse(self, response):
        name = response.meta['name']
        item_id = response.meta['item_id']
        page = response.meta['page']
        print('s')
        storemenu_json = response.body.decode()
        try:
            storemenu = json.loads(storemenu_json)
        except Exception:
            self.retry_this_poi({'name': name,
                                 'item_id': item_id,
                                 'page': page, })
            self.logger.warning(
                '%s：page%s抓取失败，已放回redis等待下次重新抓取' % (name,page))
            return

        if not isinstance(storemenu, dict):
            self.retry_this_poi({'name': name,
                                 'item_id': item_id,
                                 'page': page, })
            self.logger.warning(
                '%s：page%s抓取失败，已放回redis等待下次重新抓取' % (name, page))
            return

        item = UsStockItem()
        for poi in storemenu['rows']:
            poi['item_name']=name
            poi['item_id']=item_id
            item['detail'] = poi
            yield item
        if storemenu['page']<storemenu['total']:
            page+=1
            url, header = headers(item_id, page)
            yield scrapy.Request(url, method="GET", headers=header,
                                 callback=self.parse,
                                 dont_filter=True,
                                 meta={'name': name,
                                       'item_id': item_id,
                                       'page': page,
                                       }
                                 )
    def retry_this_poi(self, dic):
        self.r.sadd('set' + self.redis_key, json.dumps(dic).encode("utf-8"))
