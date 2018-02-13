# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import NotSupported
import requests
from requests.exceptions import ConnectionError
from urllib.parse import urlparse, urljoin


class ClimateLaciSpider(scrapy.Spider):
    name = 'climate-img'
    allowed_domains = ['climate-adapt.eea.europa.eu']
    start_urls = ['http://climate-adapt.eea.europa.eu']
    visited = set()
    img_checked = set()

    def parse(self, response):
        try:
            images = response.xpath('//img/@src').extract()
        except NotSupported:
            images = set()

        for image_url in images:
            image_url = response.urljoin(image_url)
            image_url_https = image_url.replace('http:', 'https:')
            if image_url_https not in self.img_checked:
                self.img_checked.add(image_url_https)
                try:
                    request_status_code = requests.get(image_url_https).status_code
                except ConnectionError:
                    request_status_code = 0
                if request_status_code != 200:
                    yield {
                        'img': image_url,
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
