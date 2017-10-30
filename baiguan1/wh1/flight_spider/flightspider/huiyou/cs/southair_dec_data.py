#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'fly'

import southair_dec_aes
import southair_enc_aes
import southair_dec_md5
import base64
# import crypto
# import sys
# sys.modules['Crypto'] = crypto # windows 下为小写
from Crypto.Cipher import AES
import json
import gzip
from StringIO import StringIO


def print_data(input_data):
    print "\ndata:"
    for i in range(0, len(input_data)):
        if input_data[i] < 0x10:
            print "0x0" + hex(input_data[i])[2:].upper() + ",",
        else:
            print "0x" + hex(input_data[i])[2:].upper() + ",",
        if (i + 1) % 8 == 0:
            print " ",
        if (i + 1) % 16 == 0:
            print ""


def decheckcode(base64str):
    if base64str.startswith("F"):
        base64str = base64str[1:]
    tmp_result = []
    for i in base64.b64decode(base64str):
        tmp_result.append(ord(i))
    return southair_dec_aes.de_data(tmp_result, iv=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])


def getcheckcode(datastr):
    en_result = southair_enc_aes.en_data(datastr)
    for i in range(0, len(en_result)):
        en_result[i] = chr(en_result[i])
    return "F" + base64.b64encode("".join(en_result))


def hashdata(datastr):
    if datastr.startswith("F"):
        datastr = datastr[1:]
    return southair_dec_md5.hashmd5(datastr)


def dec_resp_data(tmpdata):
    json_tmp = json.loads(tmpdata)
    title = decheckcode(json_tmp['title'])
    content = json_tmp['content']
    tmp_int = int(title[0])
    if content.startswith(title[1:1 + tmp_int]):
        _key = title[1 + tmp_int:]
        _obj = AES.new(_key, AES.MODE_CBC, '\0' * AES.block_size)
        decode_content = base64.decodestring(content)
        unpad = lambda s: s[0:-ord(s[-1])]
        buf = StringIO(unpad(_obj.decrypt(decode_content)).rstrip())
        f = gzip.GzipFile(fileobj=buf, mode="rb")
        ret = f.read()
        f.close()
        return ret
    return None


basic_data = {
    'ostype': 'and',
    'imei': '354237052324002',
    'mac': '84:2a:e3:14:a3:01',
    'model': 'Mi 4',
    'sdk': '21'
}
basic_data = {
    'ostype': 'and',
    'imei': '358239052625003',
    'mac': '8c:3a:e3:14:a3:0c',
    'model': 'Nexus 5',
    'sdk': '19'
}


def enc_req_data(tmpdata):
    tmpdata = tmpdata.strip()
    if tmpdata.startswith('{'):
        if tmpdata.endswith('}'):
            tmpdata = tmpdata[:-1]

        tmpstr = '%s,"ostype":"%s","imei":"%s","mac":"%s","model":"%s","sdk":"%s"' % (
            tmpdata, basic_data['ostype'], basic_data['imei'], basic_data['mac'], basic_data['model'],
            basic_data['sdk']
        )

        tmpcheckcode = hashdata(tmpstr + "}")

        fullstr = '%s,"checkcode":"%s"}' % (tmpstr, tmpcheckcode)

        tmpbuf = StringIO()
        f = gzip.GzipFile(fileobj=tmpbuf, mode="wb")
        f.write(getcheckcode(fullstr))
        f.close()
        tmpret = tmpbuf.getvalue()
        tmpbuf.close()

        return tmpret
    if tmpdata.startswith('<page>'):
        if tmpdata.endswith('</page>'):
            tmpdata = tmpdata[:-7]

        tmpstr = '%s<ostype>%s</ostype><imei>%s</imei><mac>%s</mac><model>%s</model><sdk>%s</sdk>' % (
            tmpdata, basic_data['ostype'], basic_data['imei'], basic_data['mac'], basic_data['model'],
            basic_data['sdk']
        )

        tmpcheckcode = hashdata(tmpstr + "</page>")

        fullstr = '%s<checkcode>%s</checkcode></page>' % (tmpstr, tmpcheckcode)
        tmpbuf = StringIO()
        f = gzip.GzipFile(fileobj=tmpbuf, mode="wb")
        f.write(getcheckcode(fullstr))
        f.close()
        tmpret = tmpbuf.getvalue()
        tmpbuf.close()
        return tmpret

if __name__ == "__main__":
    _base64str = "FqqIXuL/7w5wFrrVa39MEfxMxB0KmhR2j49H84MWm1exsX/QwUAf2Pmc44eTCWCTQwuZmwDzlSldTmNHPQrl4ucyNiyLu9QU/pTBQ37ykeccMxAhg5Wvhg1TjgHfIYIyAKkXwJZ3YOi31dDgabSwnwzCo3rgNpCZP7QyAp0ujMli6AuZKZcGlMBq+lEHocm71kXkpcG2ic1ZvH0WD0sNf6V7StdRO9aHZnbVh6s2C95VBpYR4AE5PHlgNMbrW/1bsT+joKhNJVzIMJCXAt6MXQ5wWLJoCe7LD5gdW+5xiGK55zD1q0Hr4AoBRDTaT14e6LRuuwE31ONZy5lLdi492W6ri0Pm5ISqAL2iUBkpNbAo="

    # 解密数据
    print decheckcode(_base64str)

    tmp_data = '''{"title": "FU5mjkQ7bHz3SybVZdzyxK1LN+TDIWVkE+kA2TsEQqGs=",
     "content": "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"}
     '''

    # 解密返回数据
    print dec_resp_data(tmp_data)

    # 加密请求数据
    print enc_req_data('{"CHILDNUM":"0","CITIES":[{"ARRCITY":"PEK","DEPCITY":"CAN"}],"ADULTNUM":"1","SEGTYPE":"S","ISLOGIN":false,"DATES":["20160517"]}')