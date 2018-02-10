# -*- coding: utf-8 -*-

import scrapy
import re
import urllib2
import random
from time import sleep
from scrapy import Request
from accurate_sinablog.items import AccurateSinablogItem

topK = 2


class SpiderAccurateSinablogSpider(scrapy.Spider):
    name = 'spider_accurate_sinablog'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://sina.com.cn/']

    def __init__(self, keywords=None, *args, **kwargs):
        super(SpiderAccurateSinablogSpider, self).__init__(*args, **kwargs)
        print keywords
        self.keywords = keywords
        self.start_urls = ['http://search.sina.com.cn/?by=all&ie=utf-8&q={}&c=blog&range=article'.format(keywords)]

    def parse(self, response):
        pages = 100
        for i in range(pages):
            url = response.url + '&page=' + str(i+1)
            yield Request(url=url, callback=self.article)

    def article(self, response):
        articles = response.xpath('//div[@class="box-result clearfix"]/h2/a/@href').extract()
        #artices = response.xpath('//*[@id="module_928"]/div[2]/div[1]/div[2]/div/p[1]/span[2]/a/@href').extract()
        for article in articles:
            yield Request(url=article, callback=self.detail)
    
    def detail(self, response):
        print "detail"
        item = AccurateSinablogItem()
        
        item['keywords'] = self.keywords
        item['url'] = response.url
        item['readnum'] = ' '
        title = response.xpath('//div[@class="articalTitle"]/h2/text()|//div[@class="BNE_title"]/h1/text()').extract()
        print title
        if not title:
            try:
                item['title'] = response.xpath("//*[@class='titName SG_txta']/text()").extract()[0].encode('utf-8')
            except Exception, e:
                item['title'] = ' '
            item['releaseTime'] = response.xpath('//span[@id="pub_time"]/text()|//span[@class="time SG_txtc"]/text()').extract()[0]
            tempdata = response.xpath('//div[@class="tagbox"]/a/text()').extract()
            item['tags'] = "   ".join(tempdata).encode('utf-8')
        else:
            item['title'] = title[0].encode('utf-8')
            item['releaseTime'] = response.xpath('//span[@class="time SG_txtc"]/text()').extract()[0]
            tempdata = response.xpath('//td[@class="blog_tag"]/h3/text()').extract()
            item['tags'] = "   ".join(tempdata).encode('utf-8')

        data = response.xpath('//*[@id="sina_keyword_ad_area2"]')
        item['article'] = data.xpath('string(.)').extract()[0]

        print item['title']
        print item['releaseTime']
        #print item['article']

        yield item
