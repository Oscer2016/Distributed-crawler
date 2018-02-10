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
from accurate_csdnblog.items import AccurateCsdnblogItem

topK = 2

class SpiderAccurateCsdnblogSpider(scrapy.Spider):
    name = 'spider_accurate_csdnblog'
    allowed_domains = ['csdn.net']
    start_urls = ['http://blog.csdn.net/']

    def __init__(self, keywords=None, *args, **kwargs):
        super(SpiderAccurateCsdnblogSpider, self).__init__(*args, **kwargs)
        print keywords
        self.keywords = keywords
        self.start_urls = ['http://so.csdn.net/so/search/s.do?q={}&t=blog'.format(keywords)]

    def parse(self, response):
        pdata = response.xpath('//span[@class="page-nav"]/a/text()').extract()
        pages = int(pdata[-2].strip())

        for i in xrange(pages):
            purl = response.url + "&p=" + str(i+1)
            yield Request(url=purl, callback=self.article)

    def article(self, response):
        articles = response.xpath('//dl[@class="search-list J_search"]/dt/a/@href').extract()
        for aurl in articles:
            yield Request(url=aurl, callback=self.detail)

    def detail(self, response):
        item = AccurateCsdnblogItem()

        item['url'] = response.url
        title = response.xpath('//span[@class="link_title"]/a/text()').extract()
        if not title:
            item['title'] = response.xpath('//h1[@class="csdn_top"]/text()').extract()[0].encode('utf-8')
            item['releaseTime'] = response.xpath('//span[@class="time"]/text()').extract()[0].encode('utf-8')
            item['readnum'] = response.xpath('//button[@class="btn-noborder"]/span/text()').extract()
            tempdata = response.xpath('//ul[@class="article_tags clearfix tracking-ad"]/li/a/text()').extract()
            item['tags'] = '   '.join(tempdata).encode('utf-8')
            item['sort'] = response.xpath('//div[@class="artical_tag"]/span[1]/text()').extract()[0].encode('utf-8')
        else:
            head = ""
            for t in title:
                head += t
            item['title'] = head.encode('utf-8').strip('\r\n')
            item['releaseTime'] = response.xpath('//span[@class="link_postdate"]/text()').extract()[0]
            item['readnum'] = response.xpath('//span[@class="link_view"]/text()').extract()[0].encode('utf-8')[:-9]
            tempdata = response.xpath('//span[@class="link_categories"]/a/text()').extract()
            item['tags'] = '   '.join(tempdata).encode('utf-8')
            tdata = response.xpath('//div[@class="bog_copyright"]/text()').extract()
            if not tdata:
                item['sort'] = "转载"
            else:
                item['sort'] = "原创"
            #item['sort'] = response.xpath('//div[@class="category_r"]/label/span/text()').extract()[0].encode('utf-8')
        data = response.xpath('//div[@id="article_content"]|//div[@class="markdown_views"]')
        item['article'] = data.xpath('string(.)').extract()[0]

        tags = jieba.analyse.extract_tags(item['article'],topK=topK)
        item['keywords'] = (','.join(tags))

        print item['url']
        print item['title']
        print item['sort']
        print item['keywords']

