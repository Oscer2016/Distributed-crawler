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
from accurate_cnblogs.items import AccurateCnblogsItem

topK = 2

class SpiderAccurateCnblogsSpider(scrapy.Spider):
    name = 'spider_accurate_cnblogs'
    allowed_domains = ['cnblogs.com']
    start_urls = ['https://www.cnblogs.com/']

    def __init__(self, keywords=None, *args, **kwargs):
        super(SpiderAccurateCnblogsSpider, self).__init__(*args, **kwargs)
        print keywords
        self.keywords = keywords
        self.start_urls = ['http://zzk.cnblogs.com/s?t=b&w=%s' % keywords]

    def parse(self, response):
        pages = 50
        for i in xrange(pages):
            purl = response.url + "&pageindex=" + str(i+1)
            yield Request(url=purl, callback=self.article)

    def article(self, response):
        articles = response.xpath('//h3[@class="searchItemTitle"]/a/@href').extract()
        readnums = response.xpath('//span[@class="searchItemInfo-views"]/text()').extract()
        releaseTimes = response.xpath('//span[@class="searchItemInfo-publishDate"]/text()').extract()
        article_num = len(articles)

        for i in range(article_num):
            yield Request(url=articles[i], meta={"readnum": readnums[i], "releaseTime": releaseTimes[i]}, callback=self.detail)

    def detail(self, response):
        item = AccurateCnblogsItem()
        
        item['keywords'] = self.keywords
        item['url'] = response.url
        item['readnum'] = response.meta["readnum"][3:-1]
        item['sort'] = ''
        item['releaseTime'] = response.meta["releaseTime"]
        item['title'] = response.xpath('//*[@id="cb_post_title_url"]/text()').extract()[0].encode('utf-8')
        data = response.xpath('//div[@id="cnblogs_post_body"]')
        item['article'] = data.xpath('string(.)').extract()[0]
        tags = jieba.analyse.extract_tags(item['article'],topK=topK)
        item['tags'] = ','.join(tags)
        
        print item['title']
        print item['readnum']
        print item['releaseTime']
        print item['tags']

        yield item
