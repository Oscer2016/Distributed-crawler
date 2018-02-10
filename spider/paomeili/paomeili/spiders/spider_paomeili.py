# -*- coding: utf-8 -*-

import scrapy
import re
import urllib2
from lxml import etree
from scrapy import Request
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from paomeili.items import PaomeiliItem

class SpiderPaomeiliSpider(scrapy.Spider):
    name = 'spider_paomeili'
    allowed_domains = ['paomeili.com']
    start_urls = ['http://www.paomeili.com/']

    def parse(self, response):
        sorts = response.xpath('//div[@class="cids"]/li/a/@href').extract()
        for sort in sorts:
            yield Request(url=sort, callback=self.pageturning)

    def pageturning(self, response):
        data = response.xpath('//div[@class="web_page"]/a/text()').extract()[:-1]
        pages = data[len(data)-1]
        for i in range(int(pages)):
            purl = response.url + "/{}.html".format(str(i+1))
            yield Request(url=purl, callback=self.goods)

    def goods(self, response):
        goods = response.xpath('//div[@class="item_box"]/h3/a/@href').extract()
        for gurl in goods:
            yield Request(url=gurl, callback=self.detail)

    def detail(self, response):
        item = PaomeiliItem()

        item["title"] = response.xpath('//div[@class="p_tit"]/h2/text()').extract()[0].encode('utf-8')
        item["link"] = response.url
        item["price"] = response.xpath('//div[@class="p_prc"]/b/text()').extract()[0]

        print item["title"]
        print item["link"]
        print item["price"]

        yield item
