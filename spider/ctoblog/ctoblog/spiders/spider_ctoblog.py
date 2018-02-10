# -*- coding: utf-8 -*-

import scrapy
import re
import jieba
import jieba.analyse
from docopt import docopt
from optparse import OptionParser
from scrapy.http import Request
from ctoblog.items import CtoblogItem

from kazoo.client import KazooClient
from time import sleep
import json
import threading
import random
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

topK = 2
task_dir = '/task/ctoblog/'
work_co = 0
working_list = []
hosts_list =  ['123.206.89.123:2181', '123.207.157.135:2181', '118.89.234.46:2181']
zk = KazooClient(hosts = hosts_list)


class SpiderCtoblogSpider(scrapy.Spider):
    name = 'spider_ctoblog'
    allowed_domains = ['51cto.com']
    start_urls = ['http://blog.51cto.com/expert']

    def parse(self, response):

        zk.start()
        #print "zk start"
        zode_path =  zk.create("/pid/ctoblog/node-" , ephemeral = True, sequence = True)
        myid = zode_path[-10 : ]
        mytask_dir = task_dir + "node-" + myid
        try:
            zk.create('/task/ctoblog')
            Master = True
        except :
            Master = False

        if Master == True:
            zk.create(mytask_dir)
            sleep(3)
            nodes = len(zk.get_children("/pid/ctoblog"))
            #print "my lock"
            pages = response.xpath('/html/body/div[10]/div/text()').extract()[5].split('/')[1].strip(')')
            real_nodes = zk.get_children("/task/ctoblog")
            while nodes != len(real_nodes):
                real_nodes = zk.get_children("/task/ctoblog")
                nodes = len(zk.get_children("/pid/ctoblog"))
                sleep(0.01)

            peer_tasks =int(pages) / nodes
            print "peer  %d "% peer_tasks
            i = 0
            while i < nodes:
                j = 0
                while j < peer_tasks:
                    burl = 'http://blog.51cto.com/expert.php?list-0-page-{}.html'.format(str(i*peer_tasks + j+1))
                    msg = '[{"motian":"0", "url":"' + burl + '", "level":"2", "content":"0"}]'
                    zk.create("/task/ctoblog/" + real_nodes[i] + "/task-", value = msg, sequence = True)
                    j += 1
                i += 1
        else:
            zk.create(mytask_dir)

        print "hello"
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
            print "hi"

            if task[0]['level'] == '2':
                temp = task[0]['url']
                work_co += 1
                yield Request(url= temp,meta={"task":obj_tasks,"task_dir":mytask_dir},callback=self.blogger)


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


        #for i in range(int(pages)):
        #    burl = 'http://blog.51cto.com/expert.php?list-0-page-{}.html'.format(str(i+1))
        #    yield Request(url=burl,callback=self.blogger)

    def blogger(self,response):
        #print response.url
        bloggers = response.xpath('//table/tr/td/a/@href').extract()
        #print bloggers
        j = 0
        for blogger in bloggers:
            msg = '[{"motian":"0", "url":"' + blogger + '", "level":"3", "content":"0", "from":"'+ str(os.getpid())+ '"}]'
            my_node=zk.create(response.meta["task_dir"] + "/task-", value = msg.encode("utf-8"), sequence = True)
            if j%3 == 0:
                pass #print "job is upload"
            else:
                try:
                    yield Request(url=blogger, meta = {"task":my_node,"task_dir":response.meta["task_dir"]},callback=self.total)
                except Exception,e:
                    print "yield %s" % e
            j += 1
        zk.delete(response.meta["task"])
        work_co -= 1


    def total(self, response):
        pages = response.xpath('//*[@id="layout_1"]/div[1]/div[2]/div[16]/text()').extract()[5].split('/')[1].strip(')')
        data = response.xpath('/html/head/link[3]').extract()[0]
        uid = re.findall('uid=(.*?)"',data)[0]
        j = 0
        for i in range(int(pages)):
            url = response.url + '/{}/p-{}'.format(uid,str(i+1))
            msg = '[{"motian":"0", "url":"' + url + '", "level":"4", "content":"0", "from":"'+ str(os.getpid())+ '"}]'
            my_node=zk.create(response.meta["task_dir"] + "/task-", value = msg.encode("utf-8"), sequence = True)
            if j%3 == 0:
                pass #print "job is upload"
            else:
                try:
                    yield Request(url= url,meta = {"task":my_node,"task_dir":response.meta["task_dir"]}, callback=self.article)
                except Exception,e:
                    print "yield %s" % e
                print "classfi" + str(os.getpid())#rint response.meta["task_dir"]
            j += 1
        zk.delete(response.meta["task"])
        work_co -= 2

    def article(self, response):
        articles = response.xpath('//*[@id="layout_1"]/div[1]/div[2]/div/div[1]/div[1]/h3/a/@href').extract()
        for article in articles:
            url = 'http://' + response.url.split('/')[2] + article
            msg = '[{"motian":"0", "url":"' + url + '", "level":"5", "content":"0", "from":"'+ str(os.getpid())+ '"}]'
            my_node=zk.create(response.meta["task_dir"] + "/task-", value = msg.encode("utf-8"), sequence = True)
            if i%3 == 0:
                pass #print "job is upload"
            else:
                try:
                    yield Request(url= url,meta = {"task":my_node,"task_dir":response.meta["task_dir"]}, callback=self.detail)
                except Exception,e:
                    print "yield %s" % e
                print "classfi" + str(os.getpid())#rint response.meta["task_dir"]
            i += 1
        zk.delete(response.meta["task"])
        work_co -= 4


    def detail(self, response):
        item = CtoblogItem()

        item['url'] = response.url
        item['title'] = response.xpath('//div[@class="showTitle"]/text()').extract()[1].encode('utf-8')
        item['sort'] = response.xpath('//div[@class="showType"]/a/text()').extract()[0].encode('utf-8')
        data = response.xpath('//*[@class="showContent"]')
        item['article'] = data.xpath('string(.)').extract()[0]

        tags = jieba.analyse.extract_tags(item['article'],topK=topK)
        item['keywords'] = (','.join(tags))
        
        #print item['title']
        #print item['url']
        #print item['sort']
        #print item['keywords']
        #print item['article']

        yield item
        zk.delete(response.meta["task"])
        work_co -= 8

