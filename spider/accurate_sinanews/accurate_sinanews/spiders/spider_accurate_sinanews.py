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
from accurate_sinanews.items import AccurateSinanewsItem

topK = 2

class SpiderAccurateSinanewsSpider(scrapy.Spider):
    name = 'spider_accurate_sinanews'
    allowed_domains = ['sina.com.cn']
    start_urls = ['https://news.sina.com.cn/']
    
    def __init__(self, keywords=None, *args, **kwargs):
        super(SpiderAccurateSinanewsSpider, self).__init__(*args, **kwargs)
        print keywords
        self.keywords = keywords
        self.start_urls = ['http://search.sina.com.cn/?q={}&range=title&c=news&sort=time&ie=utf-8'.format(keywords)]

    def parse(self, response):
        pdata = response.xpath('//div[@class="l_v2"]/text()').extract()[0].encode('utf-8')
        pages = int(int(re.findall('闻(.*?)篇', pdata)[0].replace(',','')) / 20)
        for i in range(pages):
            purl = response.url + "&page=" + str(i+1)
            yield Request(url=purl, callback=self.article)

    def article(self, response):
        articles = response.xpath('//div[@class="r-info r-info2"]/h2/a/@href').extract()
        for url in articles:
            yield Request(url=url, callback=self.detail)

    def detail(self, response):
        item = AccurateSinanewsItem()
        item['title'] = response.xpath('//div[@class="page-header"]/h1/text()').extract()[0].encode('utf-8')
        item['url'] = response.url
        item['releaseTime'] = response.xpath('//span[@class="time-source"]/text()').extract()[0].strip().encode('utf-8')
        tempdata = response.xpath('//div[@class="article-keywords"]/a/text()').extract()
        item['tags'] = '   '.join(tempdata).encode('utf-8')
        data = response.xpath('//*[@id="artibody"]')
        item['article'] = data.xpath('string(.)').extract()[0]
        tags = jieba.analyse.extract_tags(item['article'],topK=topK)
        item['keywords'] = (','.join(tags))

        print item['title']
        print item['url']
        print item['releaseTime']
        print item['tags']
        print item['keywords']

        yield item

