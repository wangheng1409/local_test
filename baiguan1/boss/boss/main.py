from scrapy import cmdline
import datetime
today=str(datetime.date.today())
s="scrapy crawl bossspider -s LOG_EVEL=debug -s LOG_FILE=xdf_log_%s.txt" % today
print(s)
# cmdline.execute(s.split())
cmdline.execute("scrapy crawl bossspider".split())