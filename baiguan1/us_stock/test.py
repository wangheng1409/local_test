
import pandas as pd


id_pd = pd.read_csv('baidu_order.csv', header=0, sep=',')
# print(id_pd)
s=id_pd['oid'].values.tolist()
print(s)


#
# id_pd1 = pd.read_csv('NYSE-MID-CAP-companylist-20170614.csv', header=0, sep=',')
# # print(id_pd)
# w=id_pd1['Symbol'].values.tolist()
# w=map(lambda x:x.lower().strip(),w)
# w=[x for x in w]
# print(w)