# coding: utf-8
import os
import datetime
import tornado.ioloop
import tornado.web


MAIN_PAGE = r'''
<html>
    <head>
        <title>Download File</title>
    </head>
    <body>
        <h4>成都航空</h4>
        <lable>单程特价&nbsp;&nbsp;&nbsp;</lable><a href="/static/eu_change.zip">下载地址</a>
        <h>{eu_create_time}</h>
        <br>
        <lable>预付政策&nbsp;&nbsp;&nbsp;</lable><a href="/static/eu_prepay.zip">下载地址</a>
        <h>{eu_prepay_time}</h>
        <br>
        <h4>华夏航空</h4>
        <lable>单程特价&nbsp;&nbsp;&nbsp;</lable><a href="/static/g5_change.zip">下载地址</a>
        <h>{g5_create_time}</h>
        <br>
        <lable>预付政策&nbsp;&nbsp;&nbsp;</lable><a href="/static/g5_prepay.zip">下载地址</a>
        <h>{g5_prepay_time}</h>
        <br>
        <h4>幸福航空</h4>
        <lable>单程特价&nbsp;&nbsp;&nbsp;</lable><a href="/static/jr_change.zip">下载地址</a>
        <h>{jr_create_time}</h>
        <br>
        <lable>预付政策&nbsp;&nbsp;&nbsp;</lable><a href="/static/jr_prepay.zip">下载地址</a>
        <h>{jr_prepay_time}</h>
        <br>
        <h4>厦门航空</h4>
        <lable>单程特价&nbsp;&nbsp;&nbsp;</lable><a href="/static/mf_change.zip">下载地址</a>
        <h>{mf_create_time}</h>
        <br>
        <lable>预付政策&nbsp;&nbsp;&nbsp;</lable><a href="/static/mf_prepay.zip">下载地址</a>
        <h>{mf_prepay_time}</h>
        <br>
        <h4>西藏航空</h4>
        <lable>单程特价&nbsp;&nbsp;&nbsp;</lable><a href="/static/tv_change.zip">下载地址</a>
        <h>{tv_create_time}</h>
        <br>
        <lable>预付政策&nbsp;&nbsp;&nbsp;</lable><a href="/static/tv_prepay.zip">下载地址</a>
        <h>{tv_prepay_time}</h>
        <br>
        <h4>福州航空</h4>
        <lable>单程特价&nbsp;&nbsp;&nbsp;</lable><a href="/static/fu_change.zip">下载地址</a>
        <h>{fu_create_time}</h>
        <br>
        <lable>预付政策&nbsp;&nbsp;&nbsp;</lable><a href="/static/fu_prepay.zip">下载地址</a>
        <h>{fu_prepay_time}</h>
        <br>
        <h4>河北航空</h4>
        <lable>单程特价&nbsp;&nbsp;&nbsp;</lable><a href="/static/ns_change.zip">下载地址</a>
        <h>{ns_create_time}</h>
        <br>
        <lable>预付政策&nbsp;&nbsp;&nbsp;</lable><a href="/static/ns_prepay.zip">下载地址</a>
        <h>{ns_prepay_time}</h>
    </body>
</html>
'''

settings = dict(
    static_path='/data/download',
    debug=True
)


def get_create_time(company):
    try:
        ntime = os.path.getmtime(r'/data/download/'
                                 r'%s_change.zip' % company.lower())
        date = datetime.datetime.fromtimestamp(ntime)
        xls_time = date.strftime('%Y-%m-%d %H:%M:%S')
    except:
        xls_time = ""
    return xls_time


def get_prepay_time(company):
    try:
        ntime = os.path.getmtime(r'/data/download/'
                                 r'%s_prepay.zip' % company.lower())
        date = datetime.datetime.fromtimestamp(ntime)
        xls_time = date.strftime('%Y-%m-%d %H:%M:%S')
    except:
        xls_time = ""
    return xls_time


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        params = dict(
            eu_create_time=get_create_time("EU"),
            g5_create_time=get_create_time("G5"),
            jr_create_time=get_create_time("JR"),
            mf_create_time=get_create_time("MF"),
            tv_create_time=get_create_time("TV"),
            fu_create_time=get_create_time("FU"),
            ns_create_time=get_create_time("NS"),
            eu_prepay_time=get_prepay_time("EU"),
            g5_prepay_time=get_prepay_time("G5"),
            jr_prepay_time=get_prepay_time("JR"),
            mf_prepay_time=get_prepay_time("MF"),
            tv_prepay_time=get_prepay_time("TV"),
            fu_prepay_time=get_prepay_time("FU"),
            ns_prepay_time=get_prepay_time("NS"),
        )
        res = MAIN_PAGE.format(**params)
        self.write(res)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/data/download/", tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
    ], **settings)


if __name__ == "__main__":
    app = make_app()
    app.listen(9168)
    tornado.ioloop.IOLoop.current().start()
