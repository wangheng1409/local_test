import asyncio
import aiohttp
import uvloop
from bo_lib.general import ProxyManager
pm = ProxyManager()
headers = {
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding':'gzip, deflate, br',
    'accept-language':'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
    'cache-control':'max-age=0',
    'upgrade-insecure-requests':'1',
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
}
j=0
url='https://s.2.taobao.com/list/waterfall/waterfall.htm?wp={}&_ksTS=1502424139973_130&callback=jsonp131&stype=1&catid={}&st_trust=1&ist=1'
pages = [str(i) for i in range(1000)]
catids = ["50100399"]
async def getPage(session, page,catid):
    global j
    with aiohttp.Timeout(60):
        async with session.get(url.format(page,catid), headers=headers, proxy=pm.getProxyV2()['http']) as resp:
            print(await resp.text())
            # print(await type(resp.text()))


loop = uvloop.new_event_loop()
asyncio.set_event_loop(loop)
session = aiohttp.ClientSession(loop=loop)

tasks = []
for catid in catids:
    for page in pages:
        tasks.append(getPage(session, page,catid))

loop.run_until_complete(asyncio.gather(*tasks))

loop.close()
session.close()
