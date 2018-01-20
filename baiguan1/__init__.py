
import pymongo

client = pymongo.MongoClient('mongodb://root:big_one_112358@123.59.69.66:5600')

# collection=client.ebay.ebay_us_menu_2018_01_19_detail
#
# totalcount=collection.find({}).count()
# print(totalcount)

collection=client.ebay.ebay_uk_category_cut
totalcount=collection.find({}).count()

print(totalcount)

