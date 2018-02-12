# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class HttpsCrawlerItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    climate_urls = Field()
    http_ok = Field()
    http_not_ok = Field()

    images = Field()
    locations = Field()

    url = Field()
    date = Field()
    spider = Field()
    server = Field()
    project = Field()
