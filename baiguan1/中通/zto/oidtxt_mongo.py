# !/usr/bin/env python
# -*- coding:utf-8 -*-

def LCS(x, y):
    return len(set(x)&set(y))
def deal(a,b):
    r_len = LCS(list(a), list(b))
    result_a = r_len / len(a)
    result_b = r_len / len(b)
    return min([result_a,result_b]),True if min([result_a,result_b])>0.5 else False

if  __name__ =='__main__':
    a = "Study hard, Chen Xiang"
    b= "Study,Ch en "
    p,result=deal(a,b)
    print(p,result)

    a = "雍和宫A"
    b = "雍和宫B"
    p, result = deal(a, b)
    print(p, result)

    a = "雍和宫77文创"
    b = "雍和宫七七文创"
    p, result = deal(a, b)
    print(p, result)

    a = "雍和宫77文创"
    b = "七七文创雍和宫"
    p, result = deal(a, b)
    print(p, result)