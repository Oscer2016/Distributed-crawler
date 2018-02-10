# -*- coding: utf-8 -*-

import scrapy
import re
import ssl
import urllib2
import lxml.html
from lxml import etree
from selenium import webdriver
from scrapy.http import Request
from jingdong.items import JingdongItem

from kazoo.client import KazooClient
from time import sleep
import json
import threading
import random

task_dir = '/task/huanqiunews/'
hosts_list =  ['123.206.89.123:2181', '123.207.157.135:2181', '118.89.234.46:2181']
#sleep(3)
#zk = KazooClient(hosts = hosts_list)

class SpiderJingdongSpider(scrapy.Spider):
    
    name = "spider_jingdong"
    allowed_domains = ["jd.com"]
    start_urls = ['https://www.jd.com/']
    
    def parse(self, response):

        '''
        zk.start()
        zode_path =  zk.create("/pid/huanqiunews/node-" , ephemeral = True, sequence = True)
        myid = zode_path[-10 : ]
        mytask_dir = task_dir + "node-" + myid
        print "hello"

        if zk.exists("/task/huanqiunews") == None:
            zk.create('/task/huanqiunews')
            zk.create(mytask_dir)
            sleep(3)
            nodes = len(zk.get_children("/pid/huanqiunews"))

            themes = response.xpath('//a[@class="cate_menu_lk"]/@href').extract()
            real_nodes = zk.get_children("/task/huanqiunews")
            while nodes != len(real_nodes):
                real_nodes = zk.get_children("/task/huanqiunews")
                sleep(0.01)

      
            peer_tasks = len(themes) / nodes #tot do: chu bu jun yun ru he cao zuo ??

            i = 0
            while i < nodes:
                j = 0
                while j < peer_tasks:
                    try:
                        url = "http:" + theme[i*peer_tasks + j]
                        msg = '[{"motian":"0", "url":"' + url+ '", "level":"2", "content":"0"}]'
                        zk.create("/task/huanqiunews/" + real_nodes[i] + "/task-", value = msg, sequence = True)
                    except Exception,e:
                        print "%s" % e
                    j += 1
                i += 1
        else:
            zk.create(mytask_dir)

        work_co = 0
        while True:
            if work_co > 10:
                sleep(10)
            try:
                tasks = zk.get_children(mytask_dir)
            except Exception,e:
                print "get_children %s" % e 
            while len(tasks) == 0:
                sleep(1)
                tasks = zk.get_children(mytask_dir)
            obj_tasks = mytask_dir + '/' + tasks[random.randint(0, len(tasks) - 1)]
  
            mytask_data, mytask_stat = zk.get(obj_tasks)
            
      
            task = json.loads(mytask_data)

            if task[0]['level'] == '2':
                url = task[0]['url']
                print "url-->" + url
                yield Request(url=url,callback=self.classification)
                work_co += 1
            '''

        themes = response.xpath('//a[@class="cate_menu_lk"]/@href').extract()
        #for theme in themes:
            #url = "http:" + theme
            #yield Request(url=url, callback=self.classification)
        yield Request(url='http:'+themes[0], callback=self.classification)

    def classification(self, response):
        #print response.url
        driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true','--load-images=false'])
        driver.get(response.url)
        sleep(1)
        data = driver.page_source
        tree = etree.HTML(data)
        sorts = tree.xpath('//a/@href')
        for sort in sorts:
            if sort.startswith('//list') or sort.startswith('//search'):
                yield Request(url='http:'+sort, callback=self.pageturning)
            elif sort.startswith('https://search') or sort.startswith('https://list'):
                yield Request(url=sort, callback=self.pageturning)
            elif sort.startswith('http') and sort.endswith('jd.com/'):
                yield Request(url=sort, callback=self.classification)

    def pageturning(self, response):
        #print response.url
        pages = response.xpath('//span[@class="fp-text"]/i/text()').extract()[0]
        #print pages
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
                    yield Request(url=url, callback=self.goods)
            else:
                for i in range(int(pages)):
                    url = response.url + '&page={}'.format(2*i+1)
                    #print '------>', url
                    yield Request(url=url, callback=self.goods)

    def goods(self, response):
        #print response.url
        gurls = response.xpath('//div[@class="p-name"]/a/@href').extract()
        for gurl in gurls:
            gurl = 'https:' + gurl

            
            yield Request(url=gurl, callback=self.next)

    def next(self, response):
        item = JingdongItem()
        #html = urllib2.urlopen(response.url).read()
        #tree = lxml.html.fromstring(html)
        #item["title"] = tree.cssselect("[@class='tb-main-title']/@data-title")

        item["title"] = response.xpath('//div[@class="sku-name"]/text()').extract()[0].encode('utf-8').strip()
        item["link"] = response.url
        item['shop'] = response.xpath('//div[@class="name"]/a/text()').extract()[0].encode('utf-8').strip()
        item['shopLink'] = 'https:' + response.xpath('//div[@class="name"]/a/@href').extract()[0]
        item['compositeScore'] = response.xpath('//em[@class="evaluate-grade"]/span/a/text()').extract()[0]

        tdata = response.url.split('/')
        skuids = tdata[3][:-5]
        purl = 'https://p.3.cn/prices/mgets?skuIds=J_' + skuids
        pricedata = urllib2.urlopen(purl).read()
        jdata = json.loads(pricedata)
        item["price"] = jdata[0]["p"]
        commenturl = "http://club.jd.com/comment/productPageComments.action?productId={}&score=0&sortType=5&page=0&pageSize=10".format(skuids)
        commentdata = urllib2.urlopen(commenturl).read().decode("GBK", "ignore")
        tempdata = re.findall('("content":".*?),"isTop"', commentdata)
        item['commentdata'] = ""
        for data in tempdata:
            item['commentdata'] += data.encode('utf-8')
        
        print item["title"]
        print item["link"]
        print item["shop"]
        print item["shopLink"]
        print item["compositeScore"]
        print item["price"]
        print item["commentdata"]
        
        yield item
