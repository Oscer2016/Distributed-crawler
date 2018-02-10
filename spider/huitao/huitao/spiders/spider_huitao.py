# -*- coding: utf-8 -*-

import scrapy
import re
import urllib2
from lxml import etree
from scrapy import Request
from huitao.items import HuitaoItem

class SpiderHuitaoSpider(scrapy.Spider):
    name = 'spider_huitao'
    allowed_domains = ['htjp888.com']
    start_urls = ['http://www.htjp888.com/']

    def parse(self, response):
        sorts = response.xpath('//dl[@class="nav_warp"]/dt/a/@href').extract()
        for sort in sorts[1:]:
            surl = response.url[:-1] + sort
            yield Request(url=surl, callback=self.pageturning)

    def pageturning(self, response):
        data = response.xpath('//ul[@class="pagination"]/li[12]/a/@href').extract()[0].split('=')
        pages = data[len(data)-1]
        for i in range(int(pages)):
            purl = response.url + '&page={}'.format(str(i))
            yield Request(url=purl, callback=self.goods)

    def goods(self, response):
        goods = response.xpath('//li[@class="goods-item"]/a/@href').extract()

        for t in goods:
            gurl = 'http://www.htjp888.com' + t
            yield Request(url=gurl, callback=self.detail)

    def detail(self, response):
        item = HuitaoItem()

        item["title"] = response.xpath('//span[@class="title"]/text()').extract()[0].encode('utf-8')
        item["link"] = response.url
        item["price"] = response.xpath('//div[@class="price"]/text()').extract()[0]
        
        turl = response.xpath('//div[@class="detail-row clearfix"]/a/@href').extract()[0]
        id = re.findall('&itemId=(.*?)&src', turl)[0]
        gurl = "https://item.taobao.com/item.htm?id={}".format(id)
        data = urllib2.urlopen(gurl).read().decode("GBK", "ignore")
        tree = etree.HTML(data)
         
        item['shop'] = tree.xpath('//*[@id="J_ShopInfo"]//dl/dd/strong/a/text()')[0].encode('utf-8').strip()
        item["shopLink"]  = 'http:' + tree.xpath('//*[@id="J_ShopInfo"]//dl/dd/strong/a/@href')[0]
        item['describeScore'] = tree.xpath('//div[@class="tb-shop-rate"]/dl[1]/dd/a/text()')[0].strip()
        item['serviceScore'] = tree.xpath('//div[@class="tb-shop-rate"]/dl[2]/dd/a/text()')[0].strip()
        item['logisticsScore'] = tree.xpath('//div[@class="tb-shop-rate"]/dl[3]/dd/a/text()')[0].strip()

        print item["title"]
        print item["link"]
        print item["price"]
        print item["shop"]
        print item["shopLink"]
        print item["describeScore"]
        print item["serviceScore"]
        print item["logisticsScore"]

        yield item

