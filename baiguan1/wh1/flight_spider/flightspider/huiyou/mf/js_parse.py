#!/usr/bin/env python
# -*- coding: utf-8 -*-
import execjs
import random
import time


class JSRuntime(object):
    __SOURCE = u"""
    function T(am) {
        var Z = function(ar, W) {
            return (ar << W) | (ar >>> (32 - W))
        }
        , an = function(au) {
            var ar = "", at, W;
            for (at = 7; at >= 0; at--) {
                W = (au >>> (at * 4)) & 15;
                ar += W.toString(16)
            }
            return ar
        }
        , ac, ap, ao, Y = [], ag = 1732584193, ae = 4023233417, ad = 2562383102, ab = 271733878, aa = 3285377520, al, ak, aj, ai, ah, aq, X, af = [];
        X = am.length;
        for (ap = 0; ap < X - 3; ap += 4) {
            ao = am.charCodeAt(ap) << 24 | am.charCodeAt(ap + 1) << 16 | am.charCodeAt(ap + 2) << 8 | am.charCodeAt(ap + 3);
            af.push(ao)
        }
        switch (X & 3) {
        case 0:
            ap = 2147483648;
            break;
        case 1:
            ap = am.charCodeAt(X - 1) << 24 | 8388608;
            break;
        case 2:
            ap = am.charCodeAt(X - 2) << 24 | am.charCodeAt(X - 1) << 16 | 32768;
            break;
        case 3:
            ap = am.charCodeAt(X - 3) << 24 | am.charCodeAt(X - 2) << 16 | am.charCodeAt(X - 1) << 8 | 128;
            break
        }
        af.push(ap);
        while ((af.length & 15) !== 14) {
            af.push(0)
        }
        af.push(X >>> 29);
        af.push((X << 3) & 4294967295);
        for (ac = 0; ac < af.length; ac += 16) {
            for (ap = 0; ap < 16; ap++) {
                Y[ap] = af[ac + ap]
            }
            for (ap = 16; ap <= 79; ap++) {
                Y[ap] = Z(Y[ap - 3] ^ Y[ap - 8] ^ Y[ap - 14] ^ Y[ap - 16], 1)
            }
            al = ag;
            ak = ae;
            aj = ad;
            ai = ab;
            ah = aa;
            for (ap = 0; ap <= 19; ap++) {
                aq = (Z(al, 5) + ((ak & aj) | (~ak & ai)) + ah + Y[ap] + 1518500249) & 4294967295;
                ah = ai;
                ai = aj;
                aj = Z(ak, 30);
                ak = al;
                al = aq
            }
            for (ap = 20; ap <= 39; ap++) {
                aq = (Z(al, 5) + (ak ^ aj ^ ai) + ah + Y[ap] + 1859775393) & 4294967295;
                ah = ai;
                ai = aj;
                aj = Z(ak, 30);
                ak = al;
                al = aq
            }
            for (ap = 40; ap <= 59; ap++) {
                aq = (Z(al, 5) + ((ak & aj) | (ak & ai) | (aj & ai)) + ah + Y[ap] + 2400959708) & 4294967295;
                ah = ai;
                ai = aj;
                aj = Z(ak, 30);
                ak = al;
                al = aq
            }
            for (ap = 60; ap <= 79; ap++) {
                aq = (Z(al, 5) + (ak ^ aj ^ ai) + ah + Y[ap] + 3395469782) & 4294967295;
                ah = ai;
                ai = aj;
                aj = Z(ak, 30);
                ak = al;
                al = aq
            }
            ag = (ag + al) & 4294967295;
            ae = (ae + ak) & 4294967295;
            ad = (ad + aj) & 4294967295;
            ab = (ab + ai) & 4294967295;
            aa = (aa + ah) & 4294967295
        }
        aq = an(ag) + an(ae) + an(ad) + an(ab) + an(aa);
        return aq.toLowerCase()
    }
    """

    @staticmethod
    def _pk_id(browser):
        ctx = execjs.compile(JSRuntime.__SOURCE)
        param = 'Win32{"pdf":"1","qt":"0","realp":"0","wma":"0","dir":"0","fla":"1","java":"0","gears":"0","ag":"0",' \
                '"cookie":"1","res":"1920x1080"}'
        str_time_stamp = str(int(time.time()) * 1000 + random.randint(111, 999))
        str_random_float = '%s%d' % (str(random.random())[:14], random.randint(11111, 99999))
        t = ctx.call("T", browser + param + str_time_stamp + str_random_float)[:16]
        return t, str_time_stamp


def main():
    js = JSRuntime()
    print js._pk_id("Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36")


if __name__ == "__main__":
    main()
