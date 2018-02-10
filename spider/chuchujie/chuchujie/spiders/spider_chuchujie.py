# -*- coding: utf-8 -*-

import scrapy
import re
import urllib2
from lxml import etree
from scrapy import Request
from chuchujie.items import ChuchujieItem


class SpiderChuchujieSpider(scrapy.Spider):
    name = 'spider_chuchujie'
    allowed_domains = ['www.chuchujue.com']
    start_urls = ['http://www.chuchujue.com/']

    def parse(self, response):
        sorts = response.xpath('//div[@class="area"]/a/@href').extract()
        for sort in sorts[1:]:
            yield Request(url=sort, callback=self.pageturning)

    def pageturning(self, response):
        data = response.xpath('//div[@class="list_page"]/span/a/text()').extract()
        if data:
            pages = data[-2]
        for i in range(int(pages)):
            purl = response.url + "/start-{}".format(str(i*60))
            yield Request(url=purl, callback=self.goods)

    def goods(self, response):
        goods = response.xpath('//h3[@class="stnmclass"]/a/@href').extract()
        titles = response.xpath('//em[@class="ptitle"]/a/text()').extract()
        prices = response.xpath('//span[@class="price_list_sale fl"]/em/text()').extract()
        for i in range(len(goods)):
            gurl = goods[i]
            title = titles[i]
            price = prices[i]
            yield Request(url=gurl, meta={"title":title,"price":price}, callback=self.detail)

    def detail(self, response):
        item = ChuchujieItem()

        item["title"] = response.meta["title"].encode('utf-8')
        item["link"] = response.url
        item["price"] = response.meta["price"]
        id = re.findall('&itemId=(.*?)&src', response.url)[0]
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

