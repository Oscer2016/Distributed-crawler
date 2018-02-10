# -*- coding: utf-8 -*-

import scrapy
from scrapy import Request
from accurate_taobao.items import AccurateTaobaoItem
from accurate_taobao.settings import DEFAULT_REQUEST_HEADERS
import re
import json
import urllib2

class SpiderAccuratetaobaoSpider(scrapy.Spider):
    name = 'spider_accurate_taobao'
    allowed_domains = ['taobao.com', 'tmall.com']
    start_urls = ['https://www.taobao.com/']
    
    def __init__(self, keywords=None, *args, **kwargs):
        super(SpiderAccuratetaobaoSpider, self).__init__(*args, **kwargs)
        print '您搜索的商品为:', keywords
        self.keywords = keywords
        self.start_urls = ['https://s.taobao.com/search?q=%s' % keywords]

    def parse(self, response):
        # 前50页
        for i in range(50):
            purl = response.url + "&s={}".format(str(i*44))
            yield Request(url=purl, callback=self.goods)

    def goods(self, response):
        body = response.body.decode("utf-8","ignore")

        patid = '"nid":"(.*?)"'
        allid = re.compile(patid).findall(body)
        for j in range(len(allid)):
            thisid = allid[j]
            url = "https://item.taobao.com/item.htm?id=" + str(thisid)
            yield Request(url=url,callback=self.next)

    def next(self, response):
        item = AccurateTaobaoItem()
        title = response.xpath('//h3[@class="tb-main-title"]/@data-title').extract()
        #item['shop_name'] = response.xpath('//*[@id="J_ShopInfo"]//dl/dd/strong/a/text()').extract()[0].encode('utf-8').strip()
        #shop_url = 'http:' + response.xpath('//*[@id="J_ShopInfo"]//dl/dd/strong/a/@href').extract()[0]
        #item['shop_link'] = shop_url
        #item['describe_score'] = response.xpath('//div[@class="tb-shop-rate"]/dl[1]/dd/a/text()').extract()[0].strip()
        #item['service_score'] = response.xpath('//div[@class="tb-shop-rate"]/dl[2]/dd/a/text()').extract()[0].strip()
        #item['logistics_score'] = response.xpath('//div[@class="tb-shop-rate"]/dl[3]/dd/a/text()').extract()[0].strip()

        goods_id = re.findall('id=(.*?)$', response.url)[0]
        
        headers = DEFAULT_REQUEST_HEADERS
        if not title:
            mall = '天猫商城'
            title = response.xpath('//div[@class="tb-detail-hd"]/h1/text()').extract()[0].encode('utf-8').strip()
            headers['referer'] = "https://detail.tmall.com/item.htm"
            purl = 'https://mdskip.taobao.com/core/initItemDetail.htm?&itemId={}'.format(goods_id)
            req = urllib2.Request(url=purl, headers=headers)
            res = urllib2.urlopen(req).read()
            pdata = re.findall('"postageFree":false,"price":"(.*?)","promType"', res)
            price = list(set(pdata))[0]
        else:
            mall = '淘宝商城'
            title = title[0].encode('utf-8')
            purl = "https://detailskip.taobao.com/service/getData/1/p1/item/detail/sib.htm?itemId={}&modules=price,xmpPromotion".format(goods_id)
            headers['referer'] = "https://item.taobao.com/item.htm"
            price_req = urllib2.Request(url=purl, headers=headers)
            price_res = urllib2.urlopen(price_req).read()
            pdata = list(set(re.findall('"price":"(.*?)"', price_res)))
            price = ""
            for t in pdata:
                if '-' in t:
                    price = t
                    break
            if not price:
                price = sorted(map(float, pdata))[0]

        comment_url = "https://rate.tmall.com/list_detail_rate.htm?itemId={}&sellerId=880734502&currentPage=1".format(goods_id)
        data = urllib2.urlopen(comment_url).read().decode("GBK", "ignore")
        cdata = '{' + data + '}'
        jdata = json.loads(cdata)
        comment_data = ''
        for i in range(5):
            comment_data += u"\n评价内容: " + jdata['rateDetail']['rateList'][i]['rateContent'] + u"\n评价时间:" + jdata['rateDetail']['rateList'][i]['rateDate']
        #temp_data = re.findall('("commentTime":.*?),"days"', comment_data)
        #if len(temp_data) == 0:
        #   temp_data = re.findall('("rateContent":.*?),"reply"', comment_data)
        #item['comment_data'] = ""
        #for data in temp_data:
        #    item['comment_data'] += data.encode('utf-8')
        
        item['keywords'] = self.keywords
        item['title'] = title
        item['price'] = price
        item['comment_data'] = comment_data
        item["link"] = response.url

        print '\n商品名:', item['title']
        print '此商品来自', mall
        print '价格:', item['price']
        print '商品链接:', item['link']
        print '部分评价:', item['comment_data']
        
        #yield item

