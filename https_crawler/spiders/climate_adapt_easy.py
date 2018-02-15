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
        # Rule(LinkExtractor()),
        Rule(LinkExtractor(),
             callback='parse_item', follow=True),
    )

    def parse_responses(self, responses):
        for response in responses:
            self.parse_item(response)

    def parse_item(self, response):
        i = dict()
        images = response.xpath('//img/@src').extract()
        if len(images) > 1:
            i['img'] = images
            #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
            #i['name'] = response.xpath('//div[@id="name"]').extract()
            #i['description'] = response.xpath('//div[@id="description"]').extract()
        else:
            i['img'] = [images]
        return i
