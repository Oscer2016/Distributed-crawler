# -*- coding: utf-8 -*-

import scrapy
import jieba
import jieba.analyse
from optparse import OptionParser
from docopt import docopt
from scrapy import Request
from eastnews.items import EastnewsItem
from kazoo.client import KazooClient
import json
import re
import urllib2
import threading
import random

import os
topK = 2
task_dir = '/task/taobao/'
hosts_list =  ['123.206.89.123:2181', '123.207.157.135:2181', '118.89.234.46:2181']
work_co = 0
working_list = []


class SpiderEastnewsSpider(scrapy.Spider):
    name = 'spider_eastnews'
    allowed_domains = ['eastday.com']
    start_urls = ['http://news.eastday.com']

    def parse(self, response):
        home = response.xpath('//div[@class="daohang"]/a[2]/@href').extract()
        yield Request(url=home[0],callback=self.scroll)

    def scroll(self, response):
        
        data = response.xpath('//div[@class="leftsection"]/p/a/text()').extract()
        pages = max(map(int,data[1:-2]))
        yield Request(url=response.url+'?t=true', callback=self.news)
        for i in range(pages+1):
            url = response.url[:-5] + '{}.html'.format(str(i+1))

            yield Request(url=url, callback=self.news)

    def news(self, response):
        news = response.xpath('//div[@class="leftsection"]/ul/li/a[2]/@href').extract()
        for nurl in news:

            yield Request(url=nurl, callback=self.detail)

    def detail(self, response):
        item = EastnewsItem()

        item['title'] = response.xpath('//div[@id="biaoti"]/text()').extract()[0].encode('utf-8')
        if len(item['title']) == 0:
            item['title'] = response.xpath('//p[@class="title"]/text()').extract()[0].encode('utf-8')
        item['url'] = response.url
        item['sort'] = response.xpath('//div[@class="grey12 weizhi1b lh22 fl"]/a[2]/text()').extract()[0].encode('utf-8')
        if len(item['sort']) == 0:
            item['sort'] = response.xpath('//div[@class="bread"]/text()').extract()[0].encode('utf-8')
        try:
            data = response.xpath('//div[@id="zw"]')
        except:
            data = response.xpath('//div[@class="nr"]')
        item['news'] = data.xpath('string(.)').extract()[0]

        tags = jieba.analyse.extract_tags(item['news'],topK=topK)
        item['keywords'] = (','.join(tags))

        print item['title']
        print item['url']
        print item['sort']
        print item['keywords']
        #print item['news']

        yield item
