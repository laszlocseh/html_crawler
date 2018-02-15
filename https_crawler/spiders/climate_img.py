# -*- coding: utf-8 -*-
import requests
from scrapy import Spider
from scrapy.exceptions import NotSupported
from scrapy.spiders import CrawlSpider
from requests.exceptions import ConnectionError
from urllib.parse import urljoin, urlparse


class ClimateLaciSpider(CrawlSpider):
    name = 'climate-img'
    allowed_domains = ['climate-adapt.eea.europa.eu']
    start_urls = ['http://climate-adapt.eea.europa.eu']

    visited = set()
    img_checked = dict()

    def get_url_complete(self, page, url):
        page = page.strip()
        if not page.startswith('http'):
            url_complete = urljoin(url, page)
        else:
            url_complete = page
        return url_complete

    def parse(self, response):
        """
            This section is for contracts
        @url http://climate-adapt.eea.europa.eu
        @returns items 259
        @scrapes img img_https status_code url_page_source
        """
        try:
            images = set(response.xpath('//img/@src').extract())
        except NotSupported:
            images = set()

        for image_url in images:
            image_url = self.get_url_complete(image_url, response.url)
            image_url_https = image_url.replace('http:', 'https:')
            img_url_parsed = urlparse(image_url)
            if img_url_parsed.netloc not in self.allowed_domains:
                if image_url_https not in self.img_checked:
                    try:
                        request_status_code = requests.get(image_url).status_code
                    except ConnectionError:
                        request_status_code = 0
                    self.img_checked.update({image_url_https: request_status_code})
                else:
                    request_status_code = self.img_checked.get(image_url_https, 0)
                if request_status_code:
                    yield {
                        'img': [image_url],
                        'img_https': image_url_https,
                        'status_code': request_status_code,
                        'url_page_source': response.url
                    }
        try:
            # next_pages = response.xpath('//a/@href[substring(., 1, 1) = "/" or substring(., 1, 1) = "."]').extract()
            next_pages = response.xpath('//a[not(contains(@href, "@")) and not(contains(@href, "more-events"))]/@href').extract()
            # next_pages = response.xpath('//a/@href').extract()
            next_pages = set(next_pages) - self.visited
        except NotSupported:
            next_pages = set()
        for page in next_pages:
            url_complete = self.get_url_complete(page, response.url)
            if url_complete not in self.visited:
                self.visited.add(url_complete)
                yield response.follow(page, callback=self.parse)
