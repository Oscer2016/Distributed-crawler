# -*- coding: utf-8 -*-

import re
import scrapy
from lxml import etree
from selenium import webdriver
from scrapy.http import Request
from suning.items import SuningItem
from kazoo.client import KazooClient
import json
import random
import os
from time import sleep

task_dir = '/task/suning/'
hosts_list =  ['123.206.89.123:2181', '123.207.157.135:2181', '118.89.234.46:2181']
work_co = 0
working_list = []
zk = KazooClient(hosts = hosts_list)

class SpiderSuningSpider(scrapy.Spider):
    name = 'spider_suning'
    allowed_domains = ['suning.com']
    start_urls = ['https://list.suning.com/']

    def parse(self, response):

        zk.start()
        #print "zk start"
        zode_path =  zk.create("/pid/suning/node-" , ephemeral = True, sequence = True)
        myid = zode_path[-10 : ]
        mytask_dir = task_dir + "node-" + myid
        try:
            zk.create('/task/suning')
            Master = True
        except :
            Master = False

        if Master == True:
            zk.create(mytask_dir)
            sleep(3)
            nodes = len(zk.get_children("/pid/suning"))
            sorts = response.xpath('//div[@class="t-left fl clearfix"]/a/@href').extract()
            real_nodes = zk.get_children("/task/suning")
            while nodes != len(real_nodes):
                real_nodes = zk.get_children("/task/suning")
                nodes = len(zk.get_children("/pid/suning"))
                sleep(0.01)

            peer_tasks = len(sorts) / nodes
            i = 0
            while i < nodes:
                j = 0
                while j < peer_tasks:
                    msg = '[{"motian":"0", "url":"' + 'http:' + sorts[i*peer_tasks + j] + '", "level":"2", "content":"0"}]'
                    zk.create("/task/suning/" + real_nodes[i] + "/task-", value = msg.encode('utf-8'), sequence = True)
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
                temp = task[0]['url']
                work_co += 2
                yield Request(url= temp,meta={"task":obj_tasks,"task_dir":mytask_dir},callback=self.pageturning)


            if task[0]['level'] == '3':
                temp = task[0]['url']
                work_co += 4
                yield Request(url=temp,meta={"task":obj_tasks,"task_dir":mytask_dir},callback=self.goods)
                #zk.delete(obj_tasks)

            if task[0]['level'] == '4':
                temp = task[0]['url']
                work_co += 8
                yield Request(url=temp,meta={"task":obj_tasks,"task_dir":mytask_dir},callback=self.next)
                #zk.delete(obj_tasks)
 

      

    def pageturning(self, response):
        goods = response.xpath('//strong[@id="totalNum"]/text()').extract()[0]
        pages = int(goods)/60
        gid = re.findall('(.*?)-(.*?)-.*?\.html',response.url)
        j = 0
        for i in range(pages):
            purl = '{}-{}-{}.html'.format(gid[0][0],gid[0][1],str(i))
            msg = '[{"motian":"0", "url":"' + purl + '", "level":"3", "content":"0", "from":"'+ str(os.getpid())+ '"}]'
            my_node=zk.create(response.meta["task_dir"] + "/task-", value = msg.encode("utf-8"), sequence = True)
            if j%3 == 0:
                pass #print "job is upload"
            else:
                try:
                    yield Request(url= purl,meta = {"task":my_node,"task_dir":response.meta["task_dir"]}, callback=self.goods)
                except Exception,e:
                    print "yield %s" % e
                print "classfi" + str(os.getpid())#rint response.meta["task_dir"]
            j += 1
        zk.delete(response.meta["task"])
        work_co -= 2
    def goods(self, response):
        print "goods"
        goods = response.xpath('//p[@class="sell-point"]/a/@href').extract()
        i = 0
        for good in goods:
            gurl = 'http:' + good
            #print gurl
            msg = '[{"motian":"0", "url":"' + gurl + '", "level":"4", "content":"0", "from":"'+ str(os.getpid())+ '"}]'
            my_node=zk.create(response.meta["task_dir"] + "/task-", value = msg.encode("utf-8"), sequence = True)
            if i%3 == 0:
                pass #print "job is upload"
            else:
                try:
                    yield Request(url= url,meta = {"task":my_node,"task_dir":response.meta["task_dir"]}, callback=self.next)
                except Exception,e:
                    print "yield %s" % e
                print "classfi" + str(os.getpid())#rint response.meta["task_dir"]
            i += 1
        zk.delete(response.meta["task"])
        work_co -= 4
    def next(self, response):
        print "next"
        item = SuningItem()
        item['title'] = response.xpath('//h1[@id="itemDisplayName"]/text()').extract()[0].encode('utf-8')
        item['link'] = response.url
        driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--load-images=false'])
        driver.get(response.url)
        data = driver.page_source
        tree = etree.HTML(data)
        mainprice = tree.xpath('//span[@class="mainprice"]/text()')
        smallprice = tree.xpath('//span[@class="mainprice"]/span/text()')
        if len(smallprice) == 2:
            item['price'] = mainprice[0]+smallprice[0]+mainprice[1]+smallprice[1]
        else:
            item['price'] = mainprice[0]+smallprice[0]
        #print item['title']
        #print item['link']
        #print item['price']

        yield item
        zk.delete(response.meta["task"])
        work_co -= 8
