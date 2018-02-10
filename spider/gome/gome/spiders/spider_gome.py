# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request

class SpiderGomeSpider(scrapy.Spider):
    name = 'spider_gome'
    allowed_domains = ['gome.com.cn']
    start_urls = ['http://list.gome.com.cn/']

    def parse(self, response):
        sorts = response.xpath('//div[@class="nav_list"]/a/@href').extract()
        for sort in sorts:
            surl = 'http:' + sort
            yield Request(url=surl, callback=self.pageturning)

    def pageturning(self, response):
        data = response.xpath('//span[@class="min-pager-number"]/text()').extract()[0]
        pages = data.split('/')[1]
        for i in range(int(pages)):

