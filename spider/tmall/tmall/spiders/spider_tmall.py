# -*- coding: utf-8 -*-

import scrapy
import re
import urllib2
from scrapy.http import Request
from tmall.items import TmallItem
from tmall.settings import DEFAULT_REQUEST_HEADERS

class SpiderTmallSpider(scrapy.Spider):
    name = 'spider_tmall'
    allowed_domains = ['tmall.com']
    start_urls = ['https://www.tmall.com/']

    def parse(self, response):
        themes = response.xpath('//ul[@class="normal-nav clearfix"]/li/a/@href').extract()
        for theme in themes:
            yield Request(url='https:'+theme, callback=self.classification)

    def classification(self, response):
        sorts = response.xpath('//ul[@class="cate-nav"]/li/ul/li/a/@href').extract()
        #print sorts
        for sort in sorts:
            key = re.findall('(q=.*?)&', sort)
            if not key:
                key = re.findall('(cat=.*?)&', sort)
            surl = "https://list.tmall.com/search_product.htm?" + key[0]
            yield Request(url=surl, callback=self.pageturning)

    def pageturning(self, response):
        data = response.xpath('//b[@class="ui-page-skip"]/form/text()').extract()[4].encode('utf-8')
        pages = re.findall('共(.*?)页', data)
        if not pages:
            pages = ['50']
        for i in range(int(pages[0])):
            purl = response.url + "&s={}".format(str(i*44))
            yield Request(url=purl, callback=self.goods)

    def goods(self, response):
        body = response.body.decode("utf-8","ignore")

        patid = 'data-id="(.*?)"'
        allid = re.compile(patid).findall(body)
        for id in allid:
            gurl = "https://detail.tmall.com/item.htm?id=" + str(id)
            yield Request(url=gurl, callback=self.detail)

    def detail(self, response):
        print response.url
        item = TmallItem()
        
        headers = DEFAULT_REQUEST_HEADERS
        headers['referer'] = "https://detail.tmall.com/item.htm"

        itemId = re.findall('id=(.*?)&', response.url)[0]
        priceurl = 'https://mdskip.taobao.com/core/initItemDetail.htm?&itemId=' + itemId
        req = urllib2.Request(url=priceurl, headers=headers)
        res = urllib2.urlopen(req).read()
        data = re.findall('"postageFree":false,"price":"(.*?)","promType"', res)

        item['title'] = response.xpath('//div[@class="tb-detail-hd"]/h1/text()').extract()[0].encode('utf-8').strip()
        item['link'] = response.url
        item['price'] = list(set(data))[0]
        item['shop'] = response.xpath('//a[@class="slogo-shopname"]/strong/text()').extract()[0].encode('utf-8').strip()
        item['shopLink'] = 'https:' + response.xpath('//a[@class="slogo-shopname"]/@href').extract()[0]
        item['describeScore'] = response.xpath('//div[@id="shop-info"]/div[2]/div[1]/div[2]/span/text()').extract()[0]
        item['serviceScore'] = response.xpath('//div[@id="shop-info"]/div[2]/div[2]/div[2]/span/text()').extract()[0]
        item['logisticsScore'] = response.xpath('//div[@id="shop-info"]/div[2]/div[3]/div[2]/span/text()').extract()[0]

        print item['title']
        print item['link']
        print item['shop']
        print item['shopLink']
        print item['describeScore']
        print item['serviceScore']
        print item['logisticsScore']
        
