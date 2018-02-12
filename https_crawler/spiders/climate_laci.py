# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import NotSupported
import requests
from urllib.parse import urlparse


class ClimateLaciSpider(scrapy.Spider):
    name = 'climate-laci'
    allowed_domains = ['climate-adapt.eea.europa.eu']
    start_urls = ['http://climate-adapt.eea.europa.eu/']
    visited = set()

    def parse(self, response):
        try:
            pages = response.xpath('//@href[substring(., 1, 5) = "http:"]')
        except Exception:
            pages = ()
        for href in pages:
            url = href.extract()
            url_parsed = urlparse(url)
            if url not in self.visited:
                self.visited.add(url)
                if url_parsed.netloc not in self.allowed_domains:
                    url_https = url.replace('http:', 'https:')
                    request_status_code = requests.get(url_https).status_code
                    if request_status_code != 200:
                        yield {
                            'url': url,
                            'url_https': url_https,
                            'status_code': request_status_code,
                            'url_page_source': response.url
                        }
                if url_parsed.netloc in self.allowed_domains:
                    yield response.follow(href, callback=self.parse)
