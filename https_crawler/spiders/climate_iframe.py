# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import NotSupported
import requests
from urllib.parse import urlparse, urljoin


class ClimateLaciSpider(scrapy.Spider):
    name = 'climate-iframe'
    allowed_domains = ['climate-adapt.eea.europa.eu']
    start_urls = ['http://climate-adapt.eea.europa.eu']
    visited = set()

    def parse(self, response):
        try:
            iframes = response.xpath('//iframe/@src').extract()
        except NotSupported:
            iframes = set()

        for iframe_url in iframes:
            iframe_url_https = iframe_url.replace('http:', 'https:')
            request_status_code = requests.get(iframe_url_https).status_code
            yield {
                'iframe': iframe_url,
                'iframe_https': iframe_url_https,
                'status_code': request_status_code,
                'url_page_source': response.url
            }
        try:
            next_pages = response.xpath('//@href[substring(., 1, 1) = "/"]').extract()
        except NotSupported:
            next_pages = set()
        for page in next_pages:
            url_complete = urljoin(response.url, page)
            if url_complete not in self.visited:
                self.visited.add(url_complete)
                yield response.follow(page, callback=self.parse)


        # for href in pages:
        #     url = href.extract()
        #     url_parsed = urlparse(url)
        #     if url not in self.visited:
        #         self.visited.add(url)
        #         if url_parsed.netloc not in self.allowed_domains:
        #             url_https = url.replace('http:', 'https:')
        #             request_status_code = requests.get(url_https).status_code
        #             if request_status_code:
        #                 yield {
        #                     'url': url,
        #                     'url_https': url_https,
        #                     'status_code': request_status_code,
        #                     'url_page_source': response.url
        #                 }
        #         if url_parsed.netloc in self.allowed_domains:
        #             yield response.follow(href, callback=self.parse)