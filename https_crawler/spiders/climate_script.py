# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import NotSupported
import requests
from requests.exceptions import ConnectionError
from urllib.parse import urlparse, urljoin


class ClimateLaciSpider(scrapy.Spider):
    name = 'climate-script'
    allowed_domains = ['climate-adapt.eea.europa.eu']
    start_urls = ['http://climate-adapt.eea.europa.eu']
    visited = set()
    script_checked = set()

    def parse(self, response):
        try:
            scripts = response.xpath('//script/@src').extract()
        except NotSupported:
            scripts = set()

        for script_url in scripts:
            script_url = response.urljoin(script_url.strip())
            script_url_https = script_url.replace('http:', 'https:')
            if script_url_https not in self.script_checked:
                self.script_checked.add(script_url_https)
                try:
                    request_status_code = requests.get(script_url_https).status_code
                except ConnectionError:
                    request_status_code = 0
                if request_status_code != 200:
                    yield {
                        'script': script_url,
                        'script_https': script_url_https,
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
