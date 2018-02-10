# -*- coding: utf-8 -*-

import scrapy
import re
import ssl
import urllib2
import lxml.html
import math
import jieba
import jieba.analyse
from optparse import OptionParser
from docopt import docopt
from scrapy.http import Request
from sinablog.items import SinablogItem
from kazoo.client import KazooClient
import json
import random
import os
from time import sleep 

topK = 2
task_dir = '/task/sinablog/'
work_co = 0
working_list = []
hosts_list =  ['123.206.89.123:2181', '123.207.157.135:2181', '118.89.234.46:2181']
zk = KazooClient(hosts = hosts_list)

class SpiderSinablogSpider(scrapy.Spider):
    name = "spider_sinablog"
    allowed_domains = ["sina.com.cn"]
    start_urls = ['http://blog.sina.com.cn/']

    def parse(self, response):
        #home = response.xpath("//a[@class='tit03_s tit03_selected']/@href").extract()
        home = response.xpath('//a[@data-sudaclick="dir_tab"]/@href').extract()
        yield Request(url=home[0],callback=self.classification)

    def classification(self, response):
        #print "second" + str(response.url)

        zk.start()
        #print "zk start"
        zode_path =  zk.create("/pid/sinablog/node-" , ephemeral = True, sequence = True)
        myid = zode_path[-10 : ]
        mytask_dir = task_dir + "node-" + myid
        try:
            zk.create('/task/sinablog')
            Master = True
        except :
            Master = False

        if Master == True:
            zk.create(mytask_dir)
            sleep(3)
            nodes = len(zk.get_children("/pid/sinablog"))
            #print "my lock"
            #themes = response.xpath('//ul[@class="service-bd"]/li/span/a/@href').extract()
            sorts = response.xpath('//*[@id="wrap"]/div/div/h2/span[2]/a/@href').extract()
            real_nodes = zk.get_children("/task/sinablog")
            while nodes != len(real_nodes):
                real_nodes = zk.get_children("/task/sinablog")
                real_nodes = zk.get_children("/task/sinablog")
                sleep(0.01)

            peer_tasks = len(sorts) / nodes
            print sorts
            i = 0
            while i < nodes:
                j = 0
                while j < peer_tasks:
                    msg = '[{"motian":"0", "url":"' + str(sorts[i*peer_tasks + j]) + '", "level":"2", "content":"0"}]'
                    zk.create("/task/sinablog/" + real_nodes[i] + "/task-", value = msg, sequence = True)
                    j += 1
                i += 1
        else:
            zk.create(mytask_dir)

        while True:
            global work_co
            if work_co > 70:
                sleep(10)
            try:
                tasks = zk.get_children(mytask_dir)
            except Exception,e:
                print "get_children %s" % e 
            while len(tasks) == 0:
                sleep(1)
                tasks = zk.get_children(mytask_dir)
            obj_tasks = mytask_dir + '/' + tasks[random.randint(0, len(tasks) - 1)]
            i = 0
            while obj_tasks in working_list:
                obj_tasks = mytask_dir + '/' + tasks[random.randint(0, len(tasks) - 1)]
                i += 1
                if i > 10:
                    tasks = zk.get_children(mytask_dir)
                    i = 0
            mytask_data, mytask_stat = zk.get(obj_tasks)
            
            #print "get ok"
            task = json.loads(mytask_data)
            #print "json ok"
            if task[0]['level'] == '2':
                url = task[0]['url']
                yield Request(url= url,meta={"task":obj_tasks,"task_dir":mytask_dir},callback=self.blogger)
                work_co += 1
            if task[0]['level'] == '3':
                temp = task[0]['url']
                work_co += 2
                yield Request(url=temp,meta={"task":obj_tasks,"task_dir":mytask_dir},callback=self.total)
                #zk.delete(obj_tasks)

            if task[0]['level'] == '4':
                temp = task[0]['url']
                work_co += 4
                yield Request(url=temp,meta={"task":obj_tasks,"task_dir":mytask_dir},callback=self.article)
                #zk.delete(obj_tasks)
 
            if task[0]['level'] == '5':
                temp = task[0]['url']
                work_co += 8
                yield Request(url=temp,meta={"task":obj_tasks,"task_dir":mytask_dir},callback=self.detail)
                #zk.delete(obj_tasks)

    
    def blogger(self, response):
        #print response.url
        print "blogger"
        bloggers = response.xpath('//ul/li/a[1]/@href').extract()
        genre = response.xpath('//div[@class="Path"]/span/text()').extract()[0].encode('utf-8')
        i = 0
        for blogger in bloggers:
            #print blogger
            msg = '[{"motian":"0", "url":"' + str(blogger) + '", "level":"3", "content":"0"}]'
            #print msg
            try:
                my_node=zk.create(response.meta["task_dir"] + "/task-", value = msg, sequence = True)
            except Exception,e:
                print "blogger %s"%e
            if i%3 == 0:
                pass #print "job is upload"
            else:
                yield Request(url=blogger,meta = {"item":genre, "task":my_node,"task_dir":response.meta["task_dir"]},callback=self.total)
            i += 1
        zk.delete(response.meta["task"])
        work_co -= 1
    def total(self, response):
        pageSize = 50.0
        print "total"
        total = response.xpath('//*[@id="module_3"]/div[2]/div/ul/li[1]/a/@href').extract()
        num = response.xpath('//*[@id="module_3"]/div[2]/div/ul/li[1]/em/text()').extract()
        #print str(num[0])[1:-1]
        blogNum = int(str(num[0])[1:-1])
        #print blogNum
        j = 0
        for i in range(int(math.ceil(blogNum/pageSize))):
            url = str(total[0])[:-6] + str(i+1) + ".html"
            msg = '[{"motian":"0", "url":"' + url + '", "level":"4", "content":"0"}]'
            my_node=zk.create(response.meta["task_dir"] + "/task-", value = msg, sequence = True)
            if j%3 == 0:
                pass #print "job is upload"
            else:
                yield Request(url=url,meta = {"item":response.meta["item"], "task":my_node,"task_dir":response.meta["task_dir"]}, callback=self.article)
            j += 1
        zk.delete(response.meta["task"])
        work_co -= 2
        #yield Request(url=total[0],meta={'amount':blogNum},callback=self.article)

    def article(self, response):
        print "article"
        #print response.url
        #amount = response.meta['amount']
        artices = response.xpath('//*[@id="module_928"]/div[2]/div[1]/div[2]/div/p[1]/span[2]/a/@href').extract()
        i = 0
        for article in artices:
            #print article
            msg = '[{"motian":"0", "url":"' + str(article) + '", "level":"5", "content":"0"}]'
            #print msg
            my_node=zk.create(response.meta["task_dir"] + "/task-", value = msg, sequence = True)
            if i%3 == 0:
                pass #print "job is upload"
            else:
                yield Request(url=article,meta = {"item":response.meta["item"],"task":my_node,"task_dir":response.meta["task_dir"]},callback=self.detail)
            i += 1
        zk.delete(response.meta["task"])
        work_co -= 4    
    def detail(self, response):
        print "detail"
        item = SinablogItem()
        
        item['title'] = response.xpath("//*[@class='titName SG_txta']/text()").extract()[0].encode('utf-8')[:]
        item['url'] = response.url
        data = response.xpath('//*[@id="sina_keyword_ad_area2"]')
        item['sort'] = response.meta["item"]
        item['article'] = data.xpath('string(.)').extract()[0]

        tags = jieba.analyse.extract_tags(item['article'],topK=topK)
        item['keywords'] = (','.join(tags))

        #print item['title']
        #print item['url']
        #print item['sort']
        #print item['article']
        #print item['keywords']

        yield item
        zk.delete(response.meta["task"])
        work_co -= 8
