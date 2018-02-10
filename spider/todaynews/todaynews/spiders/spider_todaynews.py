# -*- coding: utf-8 -*-
import scrapy


class SpiderTodaynewsSpider(scrapy.Spider):
    name = "spider_todaynews"
    allowed_domains = ["toutiao.com"]
    start_urls = ['http://toutiao.com/']

    def parse(self, response):
        pass
