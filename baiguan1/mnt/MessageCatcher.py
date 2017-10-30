#coding=utf-8
"""
Description:
    测试mitmproxy，抓包工具
Author:
    liuwen
Date:
    20170726
Ref:
    mitmproxy官网：
        https://mitmproxy.org
    github：
        https://github.com/mitmproxy/mitmproxy
    mitmproxy官方文档：
        http://docs.mitmproxy.org/en/stable/index.html
    mitmproxy使用python脚本定制开发（三）：
        http://blog.csdn.net/hqzxsc2006/article/details/73201280
    mitmproxy移动端代理抓包（一）：
        http://blog.csdn.net/hqzxsc2006/article/details/73199065
Usage:
    1.设置代理服务器
        1.1手机
            网络设置：
                代理IP：电脑端IP／mitmproxy运行的IP
                端口号：
            安装证书：
                手机端访问：http://mitm.it
        1.2浏览器
            同上
    2.开启mitmdump服务，执行MessageCatcher.py脚本
        mitmdump -s MessageCatcher.py -b 192.168.22.215 -p 8889
        mitmdump -s MessageCatcher.py -p 8889 # 不带'-b'参数也可
    3.分析结果
        查看分析报告report.txt
        使用Requests文件
        使用Responses文件
"""

from mitmproxy import http
from shutil import rmtree

import os

class MessageCatcher:
    """
    报文捕捉器
    """

    def __init__(self):
        # 路径
        self.dir_requests = './Requests'
        self.dir_responses = './Responses'
        self.file_report = './report.txt'

        # TODO：判断报文文件夹是否存在。已修改，待验证。
        # 若报文文件夹存在，则删除文件夹并新建；若报文文件夹不存在，则新建文件夹
        rmtree(self.dir_requests), os.makedirs(self.dir_requests) if os.path.exists(self.dir_requests) else os.makedirs(self.dir_requests)
        rmtree(self.dir_responses), os.makedirs(self.dir_responses) if os.path.exists(self.dir_responses) else os.makedirs(self.dir_responses)

        # 若报告文件存在，则删除。
        os.remove(self.file_report) if os.path.exists(self.file_report) else 0

        # 报文计数器
        self.count = 1

    def response(self, flow: http.HTTPFlow):
        """
        相应处理函数
            按编号保存request报文及response报文
        :param flow:
        :return:
        """

        # TODO: 过滤的内容类型，待补充。
        ignore_type_list = ['image', 'css', 'javascript', 'woff', 'octet-stream']

        # 若内容类型为文件，则不保存报文
        if 'Content-Type' in flow.response.headers:
            for content_type in ignore_type_list:
                if content_type in flow.response.headers.get('Content-Type'):
                    return 0

        """
        # 若内容类型为文件，则不保存报文
        if 'Content-Type' in flow.response.headers:
            if 'image' in flow.response.headers.get('Content-Type'):
                return 0
        # 若路径为文件类型，则不保存报文
        # TODO：html、jsp、asp、php等后缀不过滤，只过滤png、jpg、pdf、txt等文件。已修改，待验证。待完善。
        if ('.' in flow.request.path) and (not flow.request.path.split('.')[-1] in ['html', 'htm', 'jsp', 'asp', 'php']):
            return 0
        """

        # 保存request报文
        with open('%s/Request_%s.txt'%(self.dir_requests, self.count), 'w+') as f:
            message = """%s %s %s
%s
Cookie: %s

%s
            """ % (
                   flow.request.method, # 请求方法
                   flow.request.url,    # 地址链接
                   flow.request.http_version,   # HTTP版本
                   '\n'.join(['%s: %s'%(key, flow.request.headers.get(key)) for key in dict(flow.request.headers)]),    # Headers头部
                   ';'.join(['%s=%s'%(key, flow.request.cookies.get(key)) for key in dict(flow.request.cookies)]),      # Cookies
                   flow.request.text    # 内容
                   )
            f.write(message)

        # 保存response报文
        with open('%s/Response_%s.txt'%(self.dir_responses, self.count),'w+') as f:
            message = """%s %s %s
%s
Cookie: %s

%s
            """ % (
                   flow.response.http_version,  # HTTP版本
                   flow.response.status_code,   # 状态码
                   flow.response.get_state()['reason'].decode(),   # 状态信息
                   '\n'.join(['%s: %s' % (key, flow.response.headers.get(key)) for key in dict(flow.response.headers)]),  # Headers头部
                   ';'.join(['%s=%s' % (key, flow.response.cookies.get(key)) for key in dict(flow.response.cookies)]),    # Cookies
                   # TODO text()函数会造成编码问题。第1类编码问题：bytes与str编码不同，主要体现在字节文件（图片，pdf文件等）与字符串文件（html，json等）等差别。第2类编码问题：utf-8，gbk，gb2012等；第三类编码问题：gzip压缩编码，需要解压。
                   # TODO 暂时无法覆盖所有情况，所以只能返回btyes类型的content。待修改，待测试。
                   flow.response.content
                   #flow.response.text() if flow.response.headers.get('Content-Type') and ('charset' in flow.response.headers.get('Content-Type')) else flow.response.raw_content,        # 内容
                   #'---%s'%({item.split('=')[0]:item.split('=')[1] for item in flow.response.headers.get('Content-Type').split(';')}) if 'charset' in flow.response.headers.get('Content-Type') else '---'        # 内容
                   )
            f.write(message)

        # 生成报告文件
        with open(self.file_report, 'a+') as f:
            f.write('%s: %s\n'%(self.count, len(flow.response.get_content())))

        # 报文编号
        self.count += 1

    def __del__(self):
        """
        生成报文报告
            报文报告应包含以下内容：
                报文数量
                去重后的链接数量
                    去重需要划分等级
                        完全重复
                        地址重复
                        域名重复
                            二级域名
                            一级域名
                大概率候选报文
                    报文长度，按报文长度排序后的请求
        :return:
        """

        # 报文数量
        num_request = len(os.listdir(self.dir_requests))
        num_response = len(os.listdir(self.dir_responses))

        # 去重后的链接数量
            # 去重需要划分等级
                # 完全重复
                # 地址重复
                # 域名重复
                    # 二级域名
                    # 一级域名
        # 大概率候选报文
            # 报文长度，按报文长度排序后的请求
            # 响应类型

def start():
    return MessageCatcher()