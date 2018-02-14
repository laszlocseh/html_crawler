# -*- coding: utf-8 -*-
import requests
from scrapy import Spider
from scrapy.exceptions import NotSupported
from requests.exceptions import ConnectionError
from urllib.parse import urljoin


class ClimateLaciSpider(Spider):
    name = 'climate-img'
    allowed_domains = ['climate-adapt.eea.europa.eu']
    start_urls = ['http://climate-adapt.eea.europa.eu']
    visited = set()
    img_checked = set()

    def parse(self, response):
        """
            This section is for contracts
        @url    http://climate-adapt.eea.europa.eu
        @returns items 259
        @scrapes img img_https status_code url_page_source
        """
        try:
            images = response.xpath('//img/@src').extract()
        except NotSupported:
            images = set()

        for image_url in images:
            image_url = response.urljoin(image_url.strip())
            image_url_https = image_url.replace('http:', 'https:')
            if image_url_https not in self.img_checked:
                self.img_checked.add(image_url_https)
                try:
                    request_status_code = requests.get(image_url).status_code
                except ConnectionError:
                    request_status_code = 0
                if request_status_code:
                    yield {
                        'img': [image_url],
                        'img_https': image_url_https,
                        'status_code': request_status_code,
                        'url_page_source': response.url
                    }
        try:
            next_pages = response.xpath('//a/@href[substring(., 1, 1) = "/" or substring(., 1, 1) = "."]').extract()
        except NotSupported:
            next_pages = set()
        for page in next_pages:
            url_complete = urljoin(response.url, page)
            if url_complete not in self.visited:
                self.visited.add(url_complete)
                yield response.follow(page, callback=self.parse)
