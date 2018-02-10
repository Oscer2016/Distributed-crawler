# -*- coding: utf-8 -*-

import scrapy
import re
import urllib2
from lxml import etree
from scrapy import Request
from selenium import webdriver
from accurate_suning.items import AccurateSuningItem

class SpiderAccurateSuningSpider(scrapy.Spider):
    name = 'spider_accurate_suning'
    allowed_domains = ['suning.com']
    start_urls = ['https://www.suning.com/']

    def __init__(self, keywords=None, *args, **kwargs):
        super(SpiderAccurateSuningSpider, self).__init__(*args, **kwargs)
        print keywords
        self.keywords = keywords
        self.start_urls = ['https://search.suning.com/{}/'.format(keywords)]

    def parse(self, response):
        goods = response.xpath('//strong[@id="totalNum"]/text()').extract()[0]
        pages = int(goods)/60
        for i in range(pages):
            purl = response.url + "&cp=" + str(i)
            yield Request(url= purl, callback=self.goods)
    
    def goods(self, response):
        goods = response.xpath('//p[@class="sell-point"]/a/@href').extract()
        for good in goods:
            gurl = 'http:' + good
            yield Request(url= gurl, callback=self.next)
    
    def next(self, response):
        item = AccurateSuningItem()

        item['title'] = response.xpath('//h1[@id="itemDisplayName"]/text()').extract()[0].encode('utf-8')
        item['link'] = response.url
        item['shop'] = response.xpath('//a[@id="chead_indexUrl"]/@title').extract()[0].encode('utf-8')
        item['shopLink'] = "http:" + response.xpath('//a[@id="chead_indexUrl"]/@href').extract()[0]
        item["compositeScore"] = response.xpath('//span[@id="chead_shopStar"]/text()').extract()[0]

        driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--load-images=false'])
        driver.get(response.url)
        data = driver.page_source
        tree = etree.HTML(data)
        mainprice = tree.xpath('//span[@class="mainprice"]/text()')
        smallprice = tree.xpath('//span[@class="mainprice"]/span/text()')
        if len(smallprice) == 2:
            item['price'] = mainprice[0]+smallprice[0]+mainprice[1]+smallprice[1]
        else:
            item['price'] = mainprice[0]+smallprice[0]
        
        print item['title']
        print item['link']
        print item['price']
        print item['shop']
        print item['shopLink']
        print item['compositeScore']
