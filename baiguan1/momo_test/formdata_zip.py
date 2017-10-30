# !/usr/bin/env python
# -*- coding:utf-8 -*-

import base64
import zipfile

s='''AgPpRWihANVF4w1t+ArCLnDQZpruf93YtMYTilgMmVR7ZACNDtNYdMJvSue1Zp8j18k0xsd8t6so
47rK9BL4NemZfjmaEd0A/fM67tfLdtbrualah8LYZxCavqel7b7kRtlHyDVOkGdmfblsVKiQnL6P
Q3UlXG/bQ3+Gzeutvu7pOVfJvMcRAIvCZy3yw5f0WEkcKD55QMB39NuYn676bOTy4lte+VWFkn7P
dG12lpOjHSbuWizYaYm5pZkae237PodivQqaxZEaOO7W9azIbG4I6QeCugz1GgmqIoaSorVbszhJ
ZKFB3mf+IydGQXbd4MQvGPruRRlLR7KYEDzCV1B9+3TGiVVMc1xX/PerZw8GzMSxLgRzaGw504Pp
GRk2NTL7uJISGuH8aEBH3iN1KWbU4ryGEG3N2u6T5UafhFX8RJ5EEdT/vl7Hlw4KYHRFWM1gwkQn'''

s=base64.b64decode(s)
print(s)
f=open('formdata.zip','wb')
f.write(s)
f.close()

zf = zipfile.ZipFile('formdata.zip')
s=zf.read(zf.namelist()[0])
print(s)




