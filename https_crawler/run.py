from scrapy import cmdline

cmdline.execute("scrapy crawl climate-laci -o items.xml -s CLOSESPIDER_ITEMCOUNT=10".split())
