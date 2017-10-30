import hashlib
import hmac


def md5(p_str):
    m = hashlib.md5()
    m.update(p_str)
    return m.hexdigest()


def sha1(p_str):
    m = hashlib.sha1()
    m.update(p_str)
    return m.hexdigest()


def hmac_md5(key, data):
    keystr = []
    for i in range(0, len(key)):
        keystr.append(chr(key[i]))
    keystr = "".join(keystr)
    datastr = []
    for i in range(0, len(data)):
        datastr.append(chr(data[i]))
    datastr = "".join(datastr)
    result = hmac.new(keystr, datastr, hashlib.md5).hexdigest()
    return result


def hmac_sha1(key, data):
    keystr = []
    for i in range(0, len(key)):
        keystr.append(chr(key[i]))
    keystr = "".join(keystr)
    datastr = []
    for i in range(0, len(data)):
        datastr.append(chr(data[i]))
    datastr = "".join(datastr)
    result = hmac.new(keystr, datastr, hashlib.sha1).hexdigest()
    return result


def prf(data1, data2, data3, paramint):
    i = 1
    j = len(data1)
    if j % 2 == 0:
        k = i
    else:
        k = 0
    m = j / 2
    if k != 0:
        i = 0
    n = m + i
    array1 = data1[0:n]
    array2 = data1[n:n*2]
    array3 = data2 + data3
    return xor(prfhash(array1, array3, paramint, "HmacMD5"), prfhash(array2, array3, paramint, "HmacSHA1"))


def encrypt_hmac(data, key, typestr):
    if typestr == "HmacMD5":
        return hmac_md5(key, data)
    elif typestr == "HmacSHA1":
        return hmac_sha1(key, data)
    else:
        return None


def prfhash(data1, data2, paramint, typestr):
    array1 = []
    arraylist = [data2]
    for i in range(0, paramint):
        temp = encrypt_hmac(arraylist[len(arraylist)-1], data1, typestr)
        array3 = hexstr2intarray(temp)
        arraylist.append(array3)
        temp = encrypt_hmac(array3+data2, data1, typestr)
        temparray = hexstr2intarray(temp)
        array1 += temparray
    array2 = array1[0:paramint]
    return array2


def xor(data1, data2):
    i = len(data1)
    if i != len(data2):
        return None
    else:
        array = [0]*i
        for j in range(0, i):
            array[j] = data1[j] ^ data2[j]
        return array


def hexstr2intarray(p_str):
    arraylen = len(p_str)/2
    array = []
    for i in range(0, arraylen):
        temp = p_str[i*2:i*2+2]
        array.append(int(temp, 16))
    return array






