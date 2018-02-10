# -*- coding: utf-8 -*-

import scrapy
import re
import urllib2
from scrapy import Request
from accurate_tmall.settings import DEFAULT_REQUEST_HEADERS
from accurate_tmall.items import AccurateTmallItem

class SpiderAccuratetmallSpider(scrapy.Spider):
    name = 'spider_accurate_tmall'
    allowed_domains = ['tmall.com']
    start_urls = ['https://www.tmall.com/']

    def __init__(self, keywords=None, *args, **kwargs):
        super(SpiderAccuratetmallSpider, self).__init__(*args, **kwargs)
        print keywords
        self.keywords = keywords
        self.start_urls = ['https://list.tmall.com/search_product.htm?q=%s' % keywords]

    def parse(self, response):
        for i in range(50):
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
        item = AccurateTmallItem()
        
        headers = DEFAULT_REQUEST_HEADERS
        headers['referer'] = "https://detail.tmall.com/item.htm"

        itemId = re.findall('id=(.*?)$', response.url)[0]
        priceurl = 'https://mdskip.taobao.com/core/initItemDetail.htm?&itemId=' + itemId
        req = urllib2.Request(url=priceurl, headers=headers)
        res = urllib2.urlopen(req).read()
        print res
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
        print item['price']
        print item['shop']
        print item['shopLink']
        print item['describeScore']
        print item['serviceScore']
        print item['logisticsScore']
