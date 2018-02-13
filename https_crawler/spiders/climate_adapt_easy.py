# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Spider
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
from https_crawler.items import HttpsCrawlerItem


class ClimateAdaptEasySpider(CrawlSpider):
    name = 'climate-adapt-easy'
    allowed_domains = ['climate-adapt.eea.europa.eu']
    start_urls = ['http://climate-adapt.eea.europa.eu/']

    rules = (
        Rule(LinkExtractor(),
             callback='parse_item',
             follow=True),
    )

    def parse_item(self, response):
        i = dict()
        iframes = response.xpath('//iframe/@href[substring(., 1, 5) = "http:"]').extract()
        if iframes:
            i['href'] = iframes
            i['url_from'] = response.url
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
