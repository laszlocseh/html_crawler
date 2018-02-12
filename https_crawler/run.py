from scrapy import cmdline

cmdline.execute("scrapy crawl climate-adapt-easy -o items.xml -s CLOSESPIDER_ITEMCOUNT=10".split())
