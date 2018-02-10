# -*- coding: utf-8 -*-

import scrapy
import re
import jieba
import jieba.analyse
from optparse import OptionParser
from docopt import docopt
from scrapy import Request
from huanqiunews.items import HuanqiunewsItem

from kazoo.client import KazooClient
from time import sleep
import json
import threading
import random

topK = 2
task_dir = '/task/huanqiunews/'
work_co = 0
working_list = []
hosts_list =  ['123.206.89.123:2181', '123.207.157.135:2181', '118.89.234.46:2181']
zk = KazooClient(hosts = hosts_list)

class SpiderHuanqiunewsSpider(scrapy.Spider):
    name = 'spider_huanqiunews'
    allowed_domains = ['huanqiu.com']
    start_urls = ['http://www.huanqiu.com/']

    def parse(self, response):


        zk.start()
        zode_path =  zk.create("/pid/huanqiunews/node-" , ephemeral = True, sequence = True)
        myid = zode_path[-10 : ]
        mytask_dir = task_dir + "node-" + myid
        print "hello"
        try:
            zk.create('/task/huanqiunews')
            Master = True
        except :
            Master = False

        if Master == True:
            zk.create(mytask_dir)
            sleep(3)
            nodes = len(zk.get_children("/pid/huanqiunews"))

            themes = response.xpath('//em/a/@href').extract()
            #sorts = response.xpath('//div[@class="hd"]/h2/a/@href').extract()
            real_nodes = zk.get_children("/task/huanqiunews")
            while nodes != len(real_nodes):
                real_nodes = zk.get_children("/task/huanqiunews")
                nodes = len(zk.get_children("/pid/huanqiunews"))
                sleep(0.01)

      
            peer_tasks = len(themes) / nodes #tot do: chu bu jun yun ru he cao zuo ??

            i = 0
            while i < nodes:
                j = 0
                while j < peer_tasks:
                    try:
                        msg = '[{"motian":"0", "url":"' + themes[i*peer_tasks + j].encode('utf-8')+ '", "level":"2", "content":"0"}]'
                        zk.create("/task/huanqiunews/" + real_nodes[i] + "/task-", value = msg, sequence = True)
                    except Exception,e:
                        print "%s" % e
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
            
      
            task = json.loads(mytask_data)


            if task[0]['level'] == '2':
                temp = task[0]['url']
                work_co += 1
                yield Request(url=temp,meta={"task":obj_tasks,"task_dir":mytask_dir},callback=self.sort)


            if task[0]['level'] == '3':
                temp = task[0]['url']
                work_co += 2
                yield Request(url=temp,meta={"task":obj_tasks,"task_dir":mytask_dir},callback=self.pageturning)
                #zk.delete(obj_tasks)

            if task[0]['level'] == '4':
                temp = task[0]['url']
                work_co += 4
                yield Request(url=temp,meta={"task":obj_tasks,"task_dir":mytask_dir},callback=self.news)
                #zk.delete(obj_tasks)
 
            if task[0]['level'] == '5':
                temp = task[0]['url']
                work_co += 8
                yield Request(url=temp,meta={"task":obj_tasks,"task_dir":mytask_dir},callback=self.detail)
                #zk.delete(obj_tasks)

    def sort(self, response):
        sorts = response.xpath('//div[@class="pageBox"]/a/@href').extract()
        if not sorts:
            data = response.xpath('//div[@id="pages"]/a/text()').extract()
            pages = max(map(int,data[2:-1]))
            j = 0
            for i in range(pages):
                purl = response.url + '{}.html'.format(str(i+1))
                msg = '[{"motian":"0", "url":"' + purl + '", "level":"4", "content":"0"}]'
                my_node=zk.create(response.meta["task_dir"] + "/task-", value = msg, sequence = True)
                if j%3 == 0:
                    pass #print "job is upload"
                else:
                    yield Request(url=purl,meta = {"task":my_node,"task_dir":response.meta["task_dir"]}, callback=self.news)
                j += 1
        else: 
            j = 0
            for sort in sorts:
                msg = '[{"motian":"0", "url":"' + sort + '", "level":"3", "content":"0"}]'
                my_node=zk.create(response.meta["task_dir"] + "/task-", value = msg, sequence = True)
                if j%3 == 0:
                    pass #print "job is upload"
                else:
                    yield Request(url=sort,meta = {"task":my_node,"task_dir":response.meta["task_dir"]}, callback=self.pageturning)
                j += 1
        zk.delete(response.meta["task"])
        work_co -= 1

    def pageturning(self, response):
        data = response.xpath('//div[@id="pages"]/a/text()').extract()
        pages = max(map(int,data[2:-1]))
        j = 0
        for i in range(pages):
            purl = response.url + '{}.html'.format(str(i+1))
            msg = '[{"motian":"0", "url":"' + purl + '", "level":"4", "content":"0"}]'
            my_node=zk.create(response.meta["task_dir"] + "/task-", value = msg, sequence = True)
            if j%3 == 0:
                pass #print "job is upload"
            else:
                yield Request(url=purl,meta = {"task":my_node,"task_dir":response.meta["task_dir"]}, callback=self.news)
            j += 1
        zk.delete(response.meta["task"])
        work_co -= 2

    def news(self, response):
        news = response.xpath('//h3/a/@href').extract()
        i = 0
        for nurl in news:
            msg = '[{"motian":"0", "url":"' + nurl + '", "level":"5", "content":"0"}]'
            #print msg
            my_node=zk.create(response.meta["task_dir"] + "/task-", value = msg, sequence = True)
            if i%3 == 0:
                pass #print "job is upload"
            else:
                yield Request(url=nurl,meta = {"task":my_node,"task_dir":response.meta["task_dir"]},callback=self.detail)
            i += 1
        zk.delete(response.meta["task"])
        work_co -= 4

    def detail(self, response):
        item = HuanqiunewsItem()

        item['url'] = response.url
        item['title'] = response.xpath('//div[@class="conText"]/h1/text()').extract()[0].encode('utf-8')
        item['sort'] = response.xpath('//div[@class="topPath"]/a[2]/text()').extract()[0].encode('utf-8')
        data = response.xpath('//div[@class="text"]')
        item['news'] = data.xpath('string(.)').extract()[0]

        tags = jieba.analyse.extract_tags(item['news'],topK=topK)
        item['keywords'] = (','.join(tags))

        print item['title']
        print item['sort']
        #print item['news']
        print item['keywords']
        
        yield item
        zk.delete(response.meta["task"])
        work_co -= 8
