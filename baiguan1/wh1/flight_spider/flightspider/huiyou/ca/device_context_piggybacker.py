import random
import math
import time


class DeviceContextPiggybacker():
    def __init__(self):
        self.binaryData = ""
        self.numOutstandingBits = 0
        self.outstandingValue = 0L
        self.sensorInfo = ""
        self.sessionRandom = int(math.floor(16777216*random.random()))
        self.sessionTimestamp = long(time.time() * 1000)
        self.temp = ""
        self.textData = ""
        self.count = 0

    def get_message(self):
        l = 0L
        self.outstandingValue = l
        self.numOutstandingBits = 0
        self.binaryData = ""
        self.textData = ""
        self.sensorInfo = ""
        self.temp = ""
        self.binaryData += self.encodeNonNegativeNumber(0L)
        self.binaryData += self.writeNumber(self.sessionRandom, 0x18)
        self.binaryData += self.encodeNonNegativeNumber(self.sessionTimestamp)
        self.binaryData += self.encodeNonNegativeNumber(self.count)
        self.count += 1
        self.binaryData += self.finishEncode()
        self.sensorInfo += self.encodeBoolean(True)
        self.sensorInfo += self.encodeBoolean(True)
        self.sensorInfo += self.encodeBoolean(True)
        self.sensorInfo += self.encodeBoolean(True)
        self.sensorInfo += self.finishEncode()
        self.binaryData += self.encodeNonNegativeNumber(long(len(self.sensorInfo)))+self.sensorInfo+self.textData
        return self.binaryData

    def encodeNonNegativeNumber(self, num):
        startingLength = len(self.temp)
        moreBits = 1
        while moreBits != 0:
            out = num & 0x1F
            num >>= 5
            if num > 0:
                out |= 0x20
            else:
                moreBits = 0
            self.temp += (self.writeNumber(out, 6))
        return self.clearTemp(startingLength)

    def finishEncode(self):
        l = 0L
        if self.numOutstandingBits == 0:
            return ""
        else:
            result = self.writeNumber(l, 6 - self.numOutstandingBits)
            self.numOutstandingBits = 0
            self.outstandingValue = l
            return result

    def encodeBoolean(self, bool):
        if bool:
            i = 1
        else:
            i = 0
        return self.writeNumber(long(i), 1)


    def writeNumber(self, code, numBits):
        global numOutstandingBits
        global outstandingValue
        global temp
        i = 6
        if numBits == 0:
            return ""
        else:
            numNewBits = self.numOutstandingBits + numBits
            if numNewBits < i:
                self.outstandingValue <<= numBits
                self.outstandingValue += (long((1 << numBits) - 1)) & code
                self.numOutstandingBits = numNewBits
                return ""
            else:
                startingLength = len(self.temp)
                while numNewBits >= i:
                    charNewBits = 6 - self.numOutstandingBits
                    self.outstandingValue <<= charNewBits
                    self.outstandingValue += code >> numBits - charNewBits & (long((1 << charNewBits) - 1))
                    self.temp += (self.base64AEncode(self.outstandingValue))
                    self.outstandingValue = 0
                    self.numOutstandingBits = 0
                    numBits -= charNewBits
                    numNewBits -= 6
                self.outstandingValue = (long((1 << numNewBits) - 1)) & code
                self.numOutstandingBits = numNewBits
                return self.clearTemp(startingLength)

    def clearTemp(self, length):
        result = self.temp[length:]
        temp = self.temp[0:length]
        return result

    def base64AEncode(self, num):
        l = 0x3FL
        l1 = 0x3EL
        l2 = 0x34L
        l3 = 0x1AL
        num = long(num & l)
        if num < l3:
            ch = chr(0x41 + num)
        elif num < l2:
            ch = chr(0x61 + num - l3)
        elif num < l1:
            ch = chr(0x30 + num - l2)
        elif num == l1:
            ch = '-'
        elif num == l:
            ch = '_'
        else:
            return None
        return ch


if __name__ == "__main__":
    dcx = DeviceContextPiggybacker()
    print dcx.get_message()

