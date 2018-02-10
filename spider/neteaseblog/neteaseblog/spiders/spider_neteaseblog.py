# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request

class SpiderNeteaseblogSpider(scrapy.Spider):
    name = 'spider_neteaseblog'
    allowed_domains = ['163.com']
    start_urls = ['http://blog.163.com/blogger.html']

    def parse(self, response):
        bloggers = response.xpath('//ol[@class="cls2-list3"]/li/a/@href').extract()
        for blogger in bloggers:
            yield Request(url=blogger, callback=self.bloggers)

    def bloggers(self, response):
        #print response.url
        total = response.xpath('//p[@class="lnk"]/a/@href').extract()[0]
        yield Request(url=total, callback=self.total)

    def total(self, response):
        pages = response.xpath('//*[@id="-1"]/div[2]/div[1]/div/div[2]').extract()
        print pages
        #*[@id="-1"]/div[2]/div[1]/div/div[2]/div/div/div[3]/div/span[12]
