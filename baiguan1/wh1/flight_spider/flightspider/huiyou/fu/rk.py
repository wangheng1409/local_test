#!/usr/bin/env python
# coding:utf-8

import requests
from hashlib import md5


class RClient(object):

    def __init__(self, username, password, soft_id, soft_key):
        self.username = username
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.soft_key = soft_key
        self.base_params = {
            'username': self.username,
            'password': self.password,
            'softid': self.soft_id,
            'softkey': self.soft_key,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'ben',
        }

    def rk_create(self, im, im_type, timeout=60):
        """
        im: 图片字节
        im_type: 题目类型
        """
        params = {
            'typeid': im_type,
            'timeout': timeout,
        }
        params.update(self.base_params)
        files = {'image': ('a.png', im)}
        r = requests.post('http://api.ruokuai.com/create.json', data=params, files=files, headers=self.headers)
        return r.json()

    def rk_report_error(self, im_id):
        """
        im_id:报错题目的ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://api.ruokuai.com/reporterror.json', data=params, headers=self.headers)
        return r.json()


def get_verification_code(path):
    rc = RClient('yhjp001', 'yur140608', '68062', 'ce49e3dc528f4ae0a3fa64a721b66528')
    im = open(r'%s' % path, 'rb').read()
    return rc.rk_create(im, 3050)


if __name__ == '__main__':
    rc = RClient('', '', '67693', 'c62b58025e65472da09821c48987916a')
    im = open(r'c:\etest\imagecode.jpg', 'rb').read()
    print rc.rk_create(im, 3050)
