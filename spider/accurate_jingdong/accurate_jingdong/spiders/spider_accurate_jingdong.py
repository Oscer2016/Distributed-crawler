# -*- coding: utf-8 -*-

import scrapy
import re
import json
import urllib2
from scrapy import Request
from accurate_jingdong.items import AccurateJingdongItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class SpiderAccurateJingdongSpider(scrapy.Spider):
    name = 'spider_accurate_jingdong'
    allowed_domains = ['jd.com']
    start_urls = ['https://www.jd.com/']

    def __init__(self, keywords=None, *args, **kwargs):
        super(SpiderAccurateJingdongSpider, self).__init__(*args, **kwargs)
        print keywords
        self.keywords = keywords
        self.start_urls = ['https://search.jd.com/Search?keyword={}&enc=utf-8'.format(keywords)]

    def parse(self, response):
        print response.url
        pages = response.xpath('//span[@class="fp-text"]/i/text()').extract()[0]
        if re.findall('list',response.url):
            for i in range(int(pages)):
                url = response.url + '&page={}'.format(str(i+1))
                yield Request(url=url, callback=self.goods)
        else:
            data = re.findall('(.*?utf-8)',response.url)
            #print 'data: ', data
            if data:
                for i in range(int(pages)):
                    url = data[0] + '&page={}'.format(2*i+1)
                    #print '<><><><>', url
                    yield Request(url=url, callback=self.goods)
            else:
                for i in range(int(pages)):
                    url = response.url + '&page={}'.format(2*i+1)
                    #print '------>', url
                    yield Request(url=url, callback=self.goods)

    def goods(self, response):
        gurls = response.xpath('//div[@class="p-name p-name-type-2"]/a/@href').extract()
        for gurl in gurls:
            gurl = 'https:' + gurl
            yield Request(url=gurl, callback=self.next)

    def next(self, response):
        item = AccurateJingdongItem()
        #html = urllib2.urlopen(response.url).read()
        #tree = lxml.html.fromstring(html)
        #item["title"] = tree.cssselect("[@class='tb-main-title']/@data-title")

        item["title"] = response.xpath('//div[@class="sku-name"]/text()').extract()[0].encode('utf-8').strip()
        item["link"] = response.url
        item['shop'] = response.xpath('//div[@class="name"]/a/text()').extract()[0].encode('utf-8').strip()
        item['shopLink'] = 'https:' + response.xpath('//div[@class="name"]/a/@href').extract()[0]
        item['compositeScore'] = response.xpath('//em[@class="evaluate-grade"]/span/a/text()').extract()[0]
        

        data = response.url.split('?')[0].split('/')
        skuids = data[3][:-5]
        purl = 'https://p.3.cn/prices/mgets?&pduid={}&skuIds=J_{}'.format(skuids, skuids)
        pricedata = urllib2.urlopen(purl).read()
        jdata = json.loads(pricedata)
        item["price"] = jdata[0]["p"]
#        commenturl = "http://club.jd.com/comment/productPageComments.action?productId={}&score=0&sortType=5&page=0&pageSize=10".format(skuids)
#        commentdata = urllib2.urlopen(commenturl).read().decode("GBK", "ignore")
#        tempdata = re.findall('("content":".*?),"isTop"', commentdata)
#        item['commentdata'] = ""
#        for data in tempdata:
#            item['commentdata'] += data.encode('utf-8')

        print item["title"]
        print item["link"]
        print item["price"]
        print item["shop"]
        print item["shopLink"]
        print item["compositeScore"]
        
