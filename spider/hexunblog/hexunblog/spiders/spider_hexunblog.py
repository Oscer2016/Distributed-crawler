# -*- coding: utf-8 -*-

import scrapy
import re
import jieba
import jieba.analyse
from optparse import OptionParser
from docopt import docopt
from scrapy import Request
from hexunblog.items import HexunblogItem
from kazoo.client import KazooClient
import json
import re
import urllib2
import threading
import random
from time import sleep
import os
topK = 2
task_dir = '/task/hexunblog/'
hosts_list =  ['123.206.89.123:2181', '123.207.157.135:2181', '118.89.234.46:2181']
work_co = 0
working_list = []
zk = KazooClient(hosts = hosts_list)

class SpiderHexunblogSpider(scrapy.Spider):
    name = "spider_hexunblog"
    allowed_domains = ["hexun.com"]
    start_urls = ['http://blog.hexun.com/']

    def parse(self, response):

        zk.start()
        #print "zk start"
        zode_path =  zk.create("/pid/hexunblog/node-" , ephemeral = True, sequence = True)
        myid = zode_path[-10 : ]
        mytask_dir = task_dir + "node-" + myid
        #print "geting lock"
        try:
            zk.create('/task/hexunblog')
            Master = True
        except :
            Master = False

        if Master == True:
            zk.create(mytask_dir)
            sleep(3)
            try:
                themes = response.xpath('//ul[@class="blognav"]/li/a/@href').extract()
                nodes = len(zk.get_children("/pid/hexunblog"))
                real_nodes = zk.get_children("/task/hexunblog")
            except Exception,e:
                print "%e"%e
            print "realnodes" + str(real_nodes)
            while nodes != len(real_nodes):
                real_nodes = zk.get_children("/task/hexunblog")
                nodes = len(zk.get_children("/pid/hexunblog"))
                sleep(0.01)
             
            peer_tasks = len(themes) / nodes
            print "master is " + str(os.getpid())
            i = 0
            while i < nodes:
                j = 0
                while j < peer_tasks:
                    msg = '[{"motian":"0", "url":"' + str(themes[i*peer_tasks+j]) + '", "level":"2", "content":"0","state":"free"}]'
                    print msg
                    zk.create("/task/hexunblog/" + real_nodes[i] + "/task-", value = msg, sequence = True)
                    j += 1
                i += 1
            #zk.create(task_dir + "common")
        else:
            zk.create(mytask_dir)

        print "sleep"

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
            
            task = json.loads(mytask_data)


            #print "parse  " + str(os.getpid()) + ' '+ task[0]['level'] + task[0]['url']
            if task[0]['level'] == '2':
                temp = task[0]['url']
                work_co += 1
                yield Request(url=temp,meta={"task":obj_tasks,"task_dir":mytask_dir},callback=self.sort)




            if task[0]['level'] == '4':
                temp = task[0]['url']
                work_co += 1
                yield Request(url=temp,meta={"task":obj_tasks,"task_dir":mytask_dir},callback=self.blogger)
                #zk.delete(obj_tasks)
 
            if task[0]['level'] == '5':
                temp = task[0]['url']
                yield Request(url=temp,meta={"task":obj_tasks,"task_dir":mytask_dir},callback=self.blog)
                #zk.delete(obj_tasks)
 
            if task[0]['level'] == '7':
                temp = task[0]['url']
                work_co += 1
                yield Request(url=temp,meta={"task":obj_tasks,"task_dir":mytask_dir},callback=self.article)

            if task[0]['level'] == '8':
                temp = task[0]['url']
                work_co += 8
                yield Request(url=temp,meta={"task":obj_tasks,"task_dir":mytask_dir},callback=self.detail)


    def sort(self, response):

        sort = response.xpath('//dl[@class="h3"]/dd/a[2]/@href').extract()
        print "sort"   
        print sort[0]
        yield Request(url=sort[0], meta={"task":obj_tasks,"task_dir":mytask_dir}, callback=self.pageturning)

    def pageturning(self, response):
        print "page"
        data = response.xpath('//tr/td/a[@id="GridPager_Articles_lnkLastPage"]/@href').extract()[0]
        pages = int(re.findall('p_(.*?).html', data)[0])
        j = 0
        for i in range(pages):
            url = response.url[:-5] + '_p_{}.html'.format(str(i+1))
            msg = '[{"motian":"0", "url":"' + url + '", "level":"4", "content":"0"}]'
            #print msg
            my_node=zk.create(response.meta["task_dir"] + "/task-", value = msg, sequence = True)
            if j%3 == 0:
                pass #print "job is upload"
            else:
                yield Request(url=url,meta = {"task":my_node,"task_dir":response.meta["task_dir"]}, callback=self.blogger)
            j += 1
        zk.delete(response.meta["task"])
        work_co -= 1

    def blogger(self, response):
        print "blogger"
        bloggers = response.xpath('//div[@id="starlist"]/dl/dt/a/@href').extract()
        for burl in bloggers:
            msg = '[{"motian":"0", "url":"' + str(burl) + '", "level":"5", "content":"0"}]'
            #print msg
            my_node=zk.create(response.meta["task_dir"] + "/task-", value = msg, sequence = True)
            if i%3 == 0:
                pass #print "job is upload"
            else:
                yield Request(url=burl,meta = {"task":my_node,"task_dir":response.meta["task_dir"]},callback=self.blog)
            i += 1
        zk.delete(response.meta["task"])
        work_co -= 1

    def blog(self, response):
        print "blog"
        url = response.xpath('//*[@id="tt"]/div[1]/a/@href').extract()[0]
        yield Request(url=url, meta = {"task":my_node,"task_dir":response.meta["task_dir"]},callback=self.next)

    def next(self, response):
        print "next"
        data = response.xpath('//div[@class="PageSkip_1"]/a/text()').extract()
        pages = max(map(int,data[:-1]))
        for i in range(pages):
            url = response.url + '/p{}/default.html'.format(str(i+1))
            msg = '[{"motian":"0", "url":"' + url + '", "level":"7", "content":"0"}]'
            #print msg
            my_node=zk.create(response.meta["task_dir"] + "/task-", value = msg, sequence = True)
            if i%3 == 0:
                pass #print "job is upload"
            else:
                yield Request(url=url,meta = {"task":my_node,"task_dir":response.meta["task_dir"]},callback=self.article)
            i += 1
        zk.delete(response.meta["task"])
        work_co -= 1
    def article(self, response):
        print "articles"
        articles = response.xpath('//span[@class="ArticleTitleText"]/a/@href').extract()
        for aurl in articles:
            msg = '[{"motian":"0", "url":"' + aurl + '", "level":"8", "content":"0"}]'
            #print msg
            my_node=zk.create(response.meta["task_dir"] + "/task-", value = msg, sequence = True)
            if i%3 == 0:
                pass #print "job is upload"
            else:
                yield Request(url=aurl,meta = {"task":my_node,"task_dir":response.meta["task_dir"]},callback=self.detail)
            i += 1
        zk.delete(response.meta["task"])
        work_co -= 4
    def detail(self, response):
        item = HexunblogItem()

        item['title'] = response.xpath('//span[@class="ArticleTitleText"]/a/text()').extract()[0].encode('utf-8')
        item['url'] = response.url
        item['sort'] = response.xpath('//div[@class="ArticleClass"]/a[2]/text()').extract()[0].encode('utf-8')
        data = response.xpath('//div[@id="BlogArticleDetail"]')
        item['article'] = data.xpath('string(.)').extract()[0]
        #keywords = str(response.xpath('//div[@class="ArticleTag"]/a/text()').extract()).replace('u\'','\'')
        #item['keywords'] = keywords.decode("unicode-escape")
        tags = jieba.analyse.extract_tags(item['article'], topK=topK)
        item['keywords'] = (','.join(tags))

        print item['title']
        print item['url']
        print item['sort']
        print item['keywords']
        #print item['article']

        yield item
        zk.delete(response.meta["task"])
        work_co -= 8
