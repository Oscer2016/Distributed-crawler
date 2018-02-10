# -*- coding: utf-8 -*-

import scrapy
import jieba
import jieba.analyse
from optparse import OptionParser
from docopt import docopt
from scrapy import Request
from chinanews.items import ChinanewsItem

from kazoo.client import KazooClient
from time import sleep
import json
import threading
import random
topK = 2
task_dir = '/task/chinanews/'
work_co = 0
working_list = []
hosts_list =  ['123.206.89.123:2181', '123.207.157.135:2181', '118.89.234.46:2181']
sleep(3)
zk = KazooClient(hosts = hosts_list)

class SpiderChinanewsSpider(scrapy.Spider):
    name = 'spider_chinanews'
    allowed_domains = ['china.com']
    start_urls = ['http://news.china.com/']

    def parse(self, response):

        zk.start()
        zode_path =  zk.create("/pid/chinanews/node-" , ephemeral = True, sequence = True)
        myid = zode_path[-10 : ]
        mytask_dir = task_dir + "node-" + myid
        try:
            zk.create('/task/chinanews')
            Master = True
        except :
            Master = False

        if Master == True:
            zk.create(mytask_dir)
            sleep(3)
            nodes = len(zk.get_children("/pid/chinanews"))

            sorts = response.xpath('//div[@class="hd"]/h2/a/@href').extract()
            real_nodes = zk.get_children("/task/chinanews")
            while nodes != len(real_nodes):
                real_nodes = zk.get_children("/task/chinanews")
                nodes = len(zk.get_children("/pid/chinanews"))

                sleep(0.01)

      
            peer_tasks = len(sorts) / nodes #tot do: chu bu jun yun ru he cao zuo ??

            i = 0
            while i < nodes:
                j = 0
                while j < peer_tasks:
                    try:
                        msg = '[{"motian":"0", "url":"' + sorts[i*peer_tasks + j].encode('utf-8')+ '", "level":"2", "content":"0"}]'
                        zk.create("/task/chinanews/" + real_nodes[i] + "/task-", value = msg, sequence = True)
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
                url = task[0]['url']
                print "url-->" + url
                work_co += 2
                yield Request(url=url,meta={"task":obj_tasks,"task_dir":mytask_dir}, callback=self.pageturning )
                
            if task[0]['level'] == '3':
                temp = task[0]['url']
                work_co += 4
                yield Request(url=temp,meta={"task":obj_tasks,"task_dir":mytask_dir},callback=self.news)
                #zk.delete(obj_tasks)

            if task[0]['level'] == '4':
                temp = task[0]['url']
                work_co += 8
                yield Request(url=temp,meta={"task":obj_tasks,"task_dir":mytask_dir},callback=self.detail)
                #zk.delete(obj_tasks)
 

    def pageturning(self, response):
        pages = response.xpath('//span[@class="sumPage"]/cite/text()').extract()
        if not pages:
            data = response.xpath('//li/a/@href').extract()
            j = 0
            for url in data:
                msg = '[{"motian":"0", "url":"' + url + '", "level":"4", "content":"0"}]'
                my_node=zk.create(response.meta["task_dir"] + "/task-", value = msg, sequence = True)
                if j%3 == 0:
                    pass #print "job is upload"
                else:
                    yield Request(url=url,meta = {"task":my_node,"task_dir":response.meta["task_dir"]}, callback=self.detail)
                j += 1
        else:
            yield Request(url=response.url+'?', callback=self.news)
            j = 0
            for i in range(int(pages[0])):
                url = response.url[:-5] + '_{}.html'.format(str(i+1))
                msg = '[{"motian":"0", "url":"' + url + '", "level":"3", "content":"0"}]'
                my_node=zk.create(response.meta["task_dir"] + "/task-", value = msg, sequence = True)
                if j%3 == 0:
                    pass #print "job is upload"
                else:
                    yield Request(url=url,meta = {"task":my_node,"task_dir":response.meta["task_dir"]}, callback=self.news)
                j += 1
        zk.delete(response.meta["task"])
        work_co -= 2

    def news(self, response):
        data = response.xpath('//li/a/@href').extract()
        j = 0
        for url in data:
            msg = '[{"motian":"0", "url":"' + url + '", "level":"4", "content":"0"}]'
            my_node=zk.create(response.meta["task_dir"] + "/task-", value = msg, sequence = True)
            if j%3 == 0:
                pass #print "job is upload"
            else:
                yield Request(url=url,meta = {"task":my_node,"task_dir":response.meta["task_dir"]}, callback=self.detail)
            j += 1
        zk.delete(response.meta["task"])
        work_co -= 4

    def detail(self, response):
        print "detail"
        item = ChinanewsItem()
    
        item['url'] = response.url
        item['title'] = response.xpath('//h1[@id="chan_newsTitle"]/text()').extract()[0].encode('utf-8')
        item['sort'] = response.xpath('//div[@id="chan_breadcrumbs"]/a[2]/text()').extract()[0].encode('utf-8')
        data = response.xpath('//div[@id="chan_newsDetail"]')
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
