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
    iframe_checked = dict()

    def get_url_complete(self, page, url):
        page = page.strip()
        if not page.startswith('http'):
            url_complete = urljoin(url, page)
        else:
            url_complete = page
        return url_complete

    def parse(self, response):
        try:
            iframes = set(response.xpath('//iframe/@src').extract())
        except NotSupported:
            iframes = set()

        for iframe_url in iframes:
            iframe_url = self.get_url_complete(iframe_url, response.url)
            iframe_url_https = iframe_url.replace('http:', 'https:')
            iframe_url_parsed = urlparse(iframe_url)
            if iframe_url_parsed.netloc not in self.allowed_domains:
                if iframe_url_parsed not in self.iframe_checked:
                    try:
                        request_status_code = requests.get(iframe_url).status_code
                    except ConnectionError:
                        request_status_code = 0
                    self.iframe_checked.update({iframe_url: request_status_code})
                else:
                    request_status_code = self.iframe_checked.get(iframe_url, 0)
                if request_status_code:
                    yield {
                        'iframe': iframe_url,
                        'iframe_https': iframe_url_https,
                        'status_code': request_status_code,
                        'url_page_source': response.url
                    }
        try:
            # next_pages = response.xpath('//a/@href[substring(., 1, 1) = "/" or substring(., 1, 1) = "."]').extract()
            next_pages = response.xpath(
                '//a[not(contains(@href, "@")) and not(contains(@href, "more-events"))]/@href').extract()
            # next_pages = response.xpath('//a/@href').extract()
            next_pages = set(next_pages) - self.visited
        except NotSupported:
            next_pages = set()
        for page in next_pages:
            url_complete = self.get_url_complete(page, response.url)
            if url_complete not in self.visited:
                self.visited.add(url_complete)
                yield response.follow(page, callback=self.parse)