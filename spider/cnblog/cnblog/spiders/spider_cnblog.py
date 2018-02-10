# -*- coding: utf-8 -*-

import scrapy
import jieba
import jieba.analyse
from optparse import OptionParser
from docopt import docopt
from scrapy.http import Request
from cnblog.items import CnblogItem
from kazoo.client import KazooClient
from time import sleep
import json
import threading
import random
import os
topK = 2
task_dir = '/task/cnblog/'
work_co = 0
working_list = []
hosts_list =  ['123.206.89.123:2181', '123.207.157.135:2181', '118.89.234.46:2181']
sleep(3)
zk = KazooClient(hosts = hosts_list)

class SpiderCnblogSpider(scrapy.Spider):
    name = "spider_cnblog"
    allowed_domains = ["cnblogs.com"]
    start_urls = ['http://www.cnblogs.com/']

    def parse(self, response):

        zk.start()
        zode_path =  zk.create("/pid/cnblog/node-" , ephemeral = True, sequence = True)
        myid = zode_path[-10 : ]
        mytask_dir = task_dir + "node-" + myid
        try:
            zk.create('/task/cnblog')
            Master = True
        except :
            Master = False

        if Master == True:
            zk.create(mytask_dir)
            sleep(3)
            nodes = len(zk.get_children("/pid/cnblog"))

            sorts = response.xpath('//*[@id="cate_item"]/li/a/@href').extract()
            real_nodes = zk.get_children("/task/cnblog")
            while nodes != len(real_nodes):
                real_nodes = zk.get_children("/task/cnblog")
                nodes = len(zk.get_children("/pid/cnblog"))
                sleep(0.01)

      
            peer_tasks = len(sorts) / nodes #tot do: chu bu jun yun ru he cao zuo ??

            i = 0
            while i < nodes:
                j = 0
                while j < peer_tasks:
                    try:
                        obj_url = response.url[:-1]+sorts[i*peer_tasks + j].encode('utf-8')
                        msg = '[{"motian":"0", "url":"' + obj_url+ '", "level":"2", "content":"0"}]'
                        zk.create("/task/cnblog/" + real_nodes[i] + "/task-", value = msg, sequence = True)
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
                work_co += 2
                yield Request(url=temp,meta={"task":obj_tasks,"task_dir":mytask_dir},callback=self.total)


            if task[0]['level'] == '3':
                temp = task[0]['url']
                work_co += 4
                yield Request(url=temp,meta={"task":obj_tasks,"task_dir":mytask_dir},callback=self.article)
                #zk.delete(obj_tasks)

            if task[0]['level'] == '4':
                temp = task[0]['url']
                work_co += 8
                yield Request(url=temp,meta={"task":obj_tasks,"task_dir":mytask_dir},callback=self.detail)
                #zk.delete(obj_tasks)



    def total(self, response):
        j = 0
        for i in range(1,201):
            msg = '[{"motian":"0", "url":"' + response.url+str(i) + '", "level":"3", "content":"0", "from":"'+ str(os.getpid())+ '"}]'
            my_node=zk.create(response.meta["task_dir"] + "/task-", value = msg.encode("utf-8"), sequence = True)
            if j%3 == 0:
                pass #print "job is upload"
            else:
                try:
                    yield Request(url=response.url+str(i), meta = {"task":my_node,"task_dir":response.meta["task_dir"]},callback=self.article)
                except Exception,e:
                    print "yield %s" % e
            j += 1
        zk.delete(response.meta["task"])
        work_co -=2

    def article(self, response):
        print response.url
        articles = response.xpath('//*[@id="post_list"]/div/div[2]/h3/a/@href').extract()
        genre = response.xpath('//ul[@class="post_nav_block"]/li[2]/a/text()').extract()[0].encode('utf-8')
        i = 0
        for article in articles:
            msg = '[{"motian":"0", "url":"' + article + '", "level":"4", "content":"0", "from":"'+ str(os.getpid())+ '"}]'
            my_node=zk.create(response.meta["task_dir"] + "/task-", value = msg.encode("utf-8"), sequence = True)
            if i%3 == 0:
                pass #print "job is upload"
            else:
                try:
                    yield Request(url= article,meta = {"genre":genre,"task":my_node,"task_dir":response.meta["task_dir"]}, callback=self.detail)
                except Exception,e:
                    print "yield %s" % e
                print "classfi" + str(os.getpid())#rint response.meta["task_dir"]
            i += 1
        zk.delete(response.meta["task"])
        work_co -=4

    def detail(self, response):
        print "detail"
        item = CnblogItem()
        
        item['url'] = response.url
        item['title'] = response.xpath('//*[@id="cb_post_title_url"]/text()').extract()[0].encode('utf-8')
        item['sort'] = response.meta["genre"]
        data = response.xpath('//*[@id="cnblogs_post_body"]')
        item['article'] = data.xpath('string(.)').extract()[0]
        tags = jieba.analyse.extract_tags(item['article'],topK=topK)
        item['keywords'] = (','.join(tags))

        #print item['title']
        #print item['url']
        #print item['sort']
        #print item['article']
        #print item['keywords']

        #yield item
        zk.delete(response.meta["task"])
        work_co -=8
