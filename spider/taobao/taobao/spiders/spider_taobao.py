# -*- coding: utf-8 -*-

import os
import scrapy
import socket
import json
import re
import urllib2
import threading
import random
from time import sleep
from scrapy.http import Request
from taobao.items import TaobaoItem


class SpiderTaobaoSpider(scrapy.Spider):
    
    name = "spider_taobao"
    allowed_domains = ["taobao.com"]
    start_urls = ['https://www.taobao.com/']

    def parse(self, response):
        themes = response.xpath('//ul[@class="service-bd"]/li/a/@href').extract()
        for theme in themes:   
            yield Request(url=theme, callback=self.classification)


    def classification(self, response):
        
        sorts = response.xpath('//dl[@class="theme-bd-level2"]/dd/a/@href').extract()
        
        if len(sorts) == 0:
            yield Request(url=response.url, callback=self.pageturning)
        else:
            for sort in sorts:
                print sort
                temp = sort.split(':')
                url = 'http:' + temp[len(temp) - 1]
                try:
                    yield Request(url= url, callback=self.pageturning)
                except Exception,e:
                    print "yield %s" % e

    def pageturning(self, response):
        for i in range(30):
            purl = response.url + "&bcoffset=12&s={}".format(str(i*60))
            yield Request(url=purl, callback=self.goods)

    def goods(self, response):
        body = response.body.decode("utf-8","ignore")
        
        patid = '"nid":"(.*?)"'
        allid = re.compile(patid).findall(body)
        for j in range(len(allid)):
            thisid = allid[j]
            url = "https://item.taobao.com/item.htm?id=" + str(thisid)

            yield Request(url=url, callback=self.next)

    def next(self, response):
        item = TaobaoItem()

        item["title"] = response.xpath('//h3[@class="tb-main-title"]/@data-title').extract()[0].encode('utf-8')
        item["link"] = response.url
        item["price"] = response.xpath('//em[@class="tb-rmb-num"]/text()').extract()[0]
        item['shop'] = response.xpath('//*[@id="J_ShopInfo"]//dl/dd/strong/a/text()').extract()[0].encode('utf-8').strip()
        shop_url = 'http:' + response.xpath('//*[@id="J_ShopInfo"]//dl/dd/strong/a/@href').extract()[0]
        item['shopLink'] = shop_url
        item['describeScore'] = response.xpath('//div[@class="tb-shop-rate"]/dl[1]/dd/a/text()').extract()[0].strip()
        item['serviceScore'] = response.xpath('//div[@class="tb-shop-rate"]/dl[2]/dd/a/text()').extract()[0].strip()
        item['logisticsScore'] = response.xpath('//div[@class="tb-shop-rate"]/dl[3]/dd/a/text()').extract()[0].strip()

        thisid = re.findall('id=(.*?)$', response.url)[0]
        commenturl = "https://rate.tmall.com/list_detail_rate.htm?itemId={}&sellerId=880734502&currentPage=1".format(thisid)
        commentdata = urllib2.urlopen(commenturl).read().decode("GBK", "ignore")
        #data = re.findall('"rateList":(.*?}]),',commentdata)[0]
        #try:
        #    t = json.loads(data)
        #    print t[0]['rateContent'].encode('utf-8')
        #except Exception, e:
        #    print "transfer error: %s" % e
        tempdata = re.findall('("commentTime":.*?),"days"', commentdata)
        if len(tempdata) == 0:
            tempdata = re.findall('("rateContent":.*?),"reply"', commentdata)
        item['commentdata'] = ""
        for data in tempdata:
            item['commentdata'] += data.encode('utf-8')
        
        print item['title']
        print item['link']
        #print commenturl
        #print item['commentdata']
        #print item['price']

        #yield item
