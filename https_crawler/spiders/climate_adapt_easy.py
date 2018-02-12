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
             callback='parse_item'),
    )

    def parse_item(self, response):
        loader = ItemLoader(item=HttpsCrawlerItem(), response=response)
        loader.add_xpath('climate_urls', '//@href[substring(., 1, 5) = "http:"]')
        # i = dict()
        # i['href'] = response.xpath('//@href[substring(., 1, 5) = "http:"]').extract()
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return loader.load_item()
