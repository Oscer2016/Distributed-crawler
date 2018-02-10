# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from amazon.items import AmazonItem

class SpiderAmazonSpider(scrapy.Spider):
    name = "spider_amazon"
    allowed_domains = ["amazon.cn"]
    start_urls = ['https://www.amazon.cn/gp/site-directory/ref=nav_shopall_btn']

    def parse(self, response):
        sorts = response.xpath('//ul/li/span/span/a/@href').extract()
        for sort in sorts:
            yield Request(url="https://www.amazon.cn"+sort, callback=self.total)

    def total(self, response):
        li = response.url.split('=')
        gid = li[len(li)-1]
        pages = response.xpath('//span[@class="pagnDisabled"]/text()').extract()[0]
        for i in range(1,int(pages)+1):
            turl = "https://www.amazon.cn/s/rh=n%3A{}&page={}".format(gid,str(i))
            #print '---->turl:' + turl
            yield Request(url=turl, callback=self.goods)

    def goods(self, response):
        #print response.url
        goods = response.xpath('//*[@class="a-link-normal a-text-normal"]/@href').extract()
        for gurl in goods:
            yield Request(url=gurl, callback=self.next)
    
    def next(self, response):
        print response.url
        item = AmazonItem()
        
        item['url'] = response.url
        print item['url']
        item['title'] = response.xpath('//span[id="productTitle"]').extract()
        print item['title']
        item['price'] = response.xpath('//span[@id="priceblock_ourprice"]/text()').extract()
        
        print item['price']

        yield item
