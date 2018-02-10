# -*- coding: utf-8 -*-

import scrapy
import re
import urllib2
import lxml.html
import math
import jieba
import jieba.analyse
from optparse import OptionParser
from docopt import docopt
from scrapy.http import Request
from csdnblog.items import CsdnblogItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class SpiderCsdnblogSpider(scrapy.Spider):
    name = "spider_csdnblog"
    allowed_domains = ["csdn.net"]
    start_urls = ['http://blog.csdn.net/peoplelist.html?channelid=0&page=1']

    def parse(self, response):
        # 从所有博客专家首页开始抓取
        data = response.xpath('/html/body/div/span/text()').extract()[0]
        # 抓取页码
        pages = re.findall('共(.*?)页', str(data))[0]
        for i in range(0, int(pages)):
            # 构造博客专家翻页url
            purl = 'http://blog.csdn.net/peoplelist.html?channelid=0&page=' + str(i+1)
            yield Request(url=purl, callback=self.blogger)

    def blogger(self, response):
        # 爬取当前页博客专家url
        bloggers = response.xpath('/html/body/dl/dd/a/@href').extract()
        for burl in bloggers:
            yield Request(url=burl, callback=self.total)

    def total(self, response):
        data = response.xpath('//*[@id="papelist"]/span/text()').extract()[0]
        pages = re.findall('共(.*?)页',str(data))
        for i in range(0, int(pages[0])):
            # 构造博客专家所有博文翻页url
            purl = str(response.url) + '/article/list/' + str(i+1)
            yield Request(url= purl, callback=self.article)

    def article(self, response):
        # 爬取博主当前页所有文章url
        articles = response.xpath('//span[@class="link_title"]/a/@href').extract()
        for aurl in articles:
            url = "http://blog.csdn.net" + aurl
            yield Request(url=url, callback=self.detail)

    def detail(self, response):
        item = CsdnblogItem()

        # 爬取博文详情页信息
        item['url'] = response.url
        # 新版主题CSDN和旧版主题CSDN按照不同抓取规则抓取
        title = response.xpath('//span[@class="link_title"]/a/text()').extract()
        if not title:
            item['title'] = response.xpath('//h1[@class="csdn_top"]/text()').extract()[0].encode('utf-8')
            item['releaseTime'] = response.xpath('//span[@class="time"]/text()').extract()[0].encode('utf-8')
            item['readnum'] = response.xpath('//button[@class="btn-noborder"]/span/text()').extract()[0]
        else:
            item['title'] = title[0].encode('utf-8').strip()
            item['releaseTime'] = response.xpath('//span[@class="link_postdate"]/text()').extract()[0]
            item['readnum'] = response.xpath('//span[@class="link_view"]/text()').extract()[0].encode('utf-8')[:-9]

        # 抓取正文
        data = response.xpath('//div[@class="markdown_views"]|//div[@id="article_content"]')
        item['article'] = data.xpath('string(.)').extract()[0]

        # 用python jieba模块提取正文关键字，topK=2表示提取词频最高的两个
        tags = jieba.analyse.extract_tags(item['article'], topK=2)
        item['keywords'] = (','.join(tags))

        print "博文标题: ", item['title']
        print "博文链接: ", item['url']

        yield item

