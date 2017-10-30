import base64


class AppAuthenticityToken:
    def __init__(self):
        self.result = []

    def a1(self, pkgName, data):
        key = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCiVFO7bgcdW3KH3pKJFFyxyjP7X30j3gSVYTLiTziHRPVYqKSYHWm5ZtMRluBZsj1l41M2mwGclPpTyje4MgT9Z99aiVHsy2tBGdSKSZCzlQ/rQGNTtN3Ra5QhXUWvoreI4UQAi7BIoaV3D1qVM+TH1Ocq+TURvPV4TgC1uw3TewIDAQAB"
        length = len(data)
        i = 0
        j = 0
        while i < length:
            first = int(data[i:i + 3])
            i += 3
            second = int(data[i:i + 3])
            i += 3
            flag = data[i]
            if flag == 'N':
                j = self.processN(pkgName, j, first, second)
            elif flag == 'X':
                str = self.processX(i + 1, data)
                index = 0
                strLength = len(str)
                while index < j:
                    ch1 = str[index % strLength]
                    ch2 = self.result[index]
                    b1 = ord(ch1) & 0xFF
                    b2 = ord(ch2) & 0xFF
                    self.result[index] = chr(b1 ^ b2)
                    index += 1
                i += strLength + 1
            elif flag == 'C':
                j = self.processN(key, j, first, second)
            i += 1
        return "a" + base64.b64encode("".join(self.result))

    def processX(self, i, data):
        p = data.index('S', i)
        return data[i:p]

    def processN(self, pkgName, j, first, second):
        length = len(pkgName)
        f = first % length
        s = second % length
        if f > second % length:
            s = f
            f = second % length;
        if s < length:
            temp = pkgName[f:s + 1]
            buffer1 = self.result[0:j]
            buffer2 = self.result[j + len(temp):]
            self.result = buffer1 + list(temp) + buffer2
            j += s - f + 1
        return j


if __name__ == "__main__":
    data1 = "809125N569018N329221X3FCFC559S000438C340940X9886035FS285295N262958C834511N164300N471261C871686C301700N311431C991102X9B8F1907S433799X01D80808S117159X44D00FD4S"
    token = AppAuthenticityToken()
    ret = token.a1("com.rytong.airchina", data1)
    print ret
