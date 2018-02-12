# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
from https_crawler.items import HttpsCrawlerItem
import socket
import datetime
import re
from urllib.parse import urlparse
import requests


class ClimateAdaptSpider(Spider):
    name = 'climate-adapt'
    allowed_domains = ['climate-adapt.eea.europa.eu']
    start_urls = ['http://climate-adapt.eea.europa.eu/']
    domain_regex = re.compile(allowed_domains[0], re.IGNORECASE)

    def parse(self, response):
        """
        @url http://climate-adapt.eea.europa.eu/
        @returns items 1
        @scrapes href
        @scrapes url project spider server date
        """
        loader = ItemLoader(item=HttpsCrawlerItem(), response=response)
        urls = response.xpath('//@href[substring(., 1, 5) = "http:"]').extract()
        for url in urls:
            url_parsed = urlparse(url)
            if url_parsed.netloc in self.allowed_domains:
                yield Request(url)
                loader.add_value('climate_urls', url, MapCompose(str.strip))
            else:
                ok = True
                url_https = url.replace("http:", "https:")
                # request_https = requests.get(url_https)
                # if request_https.status_code == 200:
                #     request_http = requests.get(url)
                #     if request_http.status_code == 200 and request_http.content == request_https.content:
                #         ok = True
                if ok:
                    loader.add_value('http_ok', url_https, MapCompose(str.strip))
                else:
                    loader.add_value('http_not_ok', url_https, MapCompose(str.strip))
        loader.add_value('url', response.url)
        return loader.load_item()
