# -*- coding: utf-8 -*-
import scrapy


class SpiderDangdangSpider(scrapy.Spider):
    name = "spider_dangdang"
    allowed_domains = ["dangdang.com"]
    start_urls = ['http://www.dangdang.com/']

    def parse(self, response):

