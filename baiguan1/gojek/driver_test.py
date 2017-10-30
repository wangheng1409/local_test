import requests

headers={
    'X-Location':'UNKNOWN',
    'X-AppVersion':'2.22.1',
    'X-UniqueId':'49aa2544df08bdba',
    'X-User-Locale':'en_ID',
    'X-Platform':'Android',
    'X-AppId':'com.gojek.app',
    'Accept-Language':'en-ID',
    'X-PushTokenType':'GCM',
    'X-DeviceToken':'eidOuaqI9Pg:APA91bEqtMyno6fZTOpPp9SYp5ZqfehNmLwlU-DcOHWTnAamBEjyKf1t8UJOD-v9AF5S74Ggdt90g85pK9Ly0gqJC-JNvx-G4bZvLDJX7vTd73O9DJB8DI6e1bcUb6mtqV8__Mdt93VT',
    'X-Instance-Token':	'd505CdV9gLQ:APA91bGPtmogx2hvNkO5PjdiX6fYTFvOi_4eyPAAQLRMkj_SMamAiTXPOk1QSffLwU7fXB1DcLdbzQQgogYatf3LdNp-5FykCqNeAdgz6aT1RBi7quBObJYezqAKdZm-SXRgUXMOTDK8',
    'Authorization':'Bearer b3b1ef58-8746-4219-8cc5-ac90ce93f3f4',
    'user-uuid':'556922906',
    'Host':'api.gojekapi.com',
    'Connection':'Keep-Alive',
    'Accept-Encoding':'gzip',
    'User-Agent':'okhttp/3.2.0',
    'If-Modified-Since':'Mon, 12 Jun 2017 05:34:14 GMT'

}

url='https://api.gojekapi.com/gojek/service_type/19/drivers/nearby?location=-6.175175976185616,106.82853508740664'

ret=requests.get(url,headers=headers,verify=False).text
print(ret)