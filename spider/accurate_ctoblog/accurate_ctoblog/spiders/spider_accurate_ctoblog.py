# -*- coding: utf-8 -*-

import scrapy
import re
import urllib2
import random
import jieba
import jieba.analyse
from optparse import OptionParser
from docopt import docopt
from time import sleep
from scrapy import Request
from accurate_ctoblog.items import AccurateCtoblogItem

topK = 2

class SpiderAccurateCtoblogSpider(scrapy.Spider):
    name = 'spider_accurate_ctoblog'
    allowed_domains = ['51cto.com']
    start_urls = ['http://www.blog.51cto.com/']

    def __init__(self, keywords=None, *args, **kwargs):
        super(SpiderAccurateCtoblogSpider, self).__init__(*args, **kwargs)
        print keywords
        self.keywords = keywords
        self.start_urls = ['http://so.51cto.com/?project=blog&sort=time&keywords={}'.format(keywords)]

    def parse(self, response):
        pages = 50
        for i in xrange(pages):
            purl = response.url + "&p=" + str(i+1)
            yield Request(url=purl, callback=self.article)

    def article(self, response):
        articles = response.xpath('//div[@class="res-doc"]/h2/a/@href').extract()
        for url in articles:
            yield Request(url=url, callback=self.detail)

    def detail(self, response):
        item = AccurateCtoblogItem()

        item['url'] = response.url
        item['keywords'] = self.keywords
        item['releaseTime'] = response.xpath('//span[@class="artTime"]/text()').extract()
        item['title'] = response.xpath('//div[@class="showTitle"]/text()').extract()[1].encode('utf-8')
        item['sort'] = response.xpath('//div[@class="showType"]/a/text()').extract()[0].encode('utf-8')
        data = response.xpath('//*[@class="showContent"]')
        item['article'] = data.xpath('string(.)').extract()[0]

        tags = jieba.analyse.extract_tags(item['article'],topK=topK)
        item['tags'] = (','.join(tags))
        
        print item['title']
        print item['url']
        print item['releaseTime']
        print item['sort']
        print item['tags']

        yield item
