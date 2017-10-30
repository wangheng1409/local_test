import requests
import random
import time
import json
from lichao_test import pytesseract
from PIL import Image

session=requests.session()
f=open('b.png','wb')
f.write(session.get('http://hotels.huazhu.com/Blur/Pic?b=6fd7218006bf4dbabf8c4f8b9413e963',verify=False).content)
f.close()
pil_im=Image.open('b.png').convert('L')
pil_im.show()
time.sleep(2)
def initTable(threshold=100):
     table = []
     for i in range(256):
         if i < threshold:
             table.append(0)
         else:
             table.append(1)
     return table
binaryImage = pil_im.point(initTable(), '1')
binaryImage.show()
vcode = pytesseract.image_to_string(binaryImage)
print (vcode)

