# -*- coding: utf-8 -*-

import scrapy
import re
import ssl
import urllib2
import math
import signal
import jieba
import jieba.analyse
from optparse import OptionParser
from docopt import docopt
from lxml import etree
from scrapy.http import Request
from sinanews.items import SinanewsItem

from kazoo.client import KazooClient
import random
from time import sleep
import json
import os

topK = 2
task_dir = '/task/sinanews/'
work_co = 0
working_list = []
hosts_list =  ['123.206.89.123:2181', '123.207.157.135:2181', '118.89.234.46:2181']
zk = KazooClient(hosts = hosts_list)

class SpiderSinanewsSpider(scrapy.Spider):
    name = "spider_sinanews"
    allowed_domains = ["sina.com.cn"]
    start_urls = ['http://news.sina.com.cn/']

    def parse(self, response):
        home = response.xpath('//*[@id="blk_cNav2_01"]/div/a[1]/@href').extract()
        yield Request(url=home[0],callback=self.scroll)

    def scroll(self, response):

        zk.start()
        #print "zk start"
        zode_path =  zk.create("/pid/sinanews/node-" , ephemeral = True, sequence = True)
        myid = zode_path[-10 : ]
        mytask_dir = task_dir + "node-" + myid
        try:
            zk.create('/task/sinanews')
            Master = True
        except :
            Master = False

        if Master == True:
            zk.create(mytask_dir)
            sleep(3)
            nodes = len(zk.get_children("/pid/sinanews"))
            #print "my lock"
            data = response.xpath('//*[@id="d_list"]/div/a[12]/@href').extract()
            pages = int(re.findall('page=(.*?)&',data[0])[0])*0.82
            #themes = response.xpath('//ul[@class="service-bd"]/li/span/a/@href').extract()
            real_nodes = zk.get_children("/task/sinanews")
            while nodes != len(real_nodes):
                real_nodes = zk.get_children("/task/sinanews")
                nodes = len(zk.get_children("/pid/sinanews"))
                sleep(0.01)

            peer_tasks = int(pages) / nodes
            i = 0
            while i < nodes:
                j = 0
                while j < peer_tasks:
                    detail_url = "http://roll.news.sina.com.cn/interface/rollnews_ch_out_interface.php?col=89&num=60&page=" + str(i*peer_tasks + j + 1)
                    msg = '[{"motian":"0", "url":"' + detail_url + '", "level":"2", "content":"0"}]'
                    zk.create("/task/sinanews/" + real_nodes[i] + "/task-", value = msg, sequence = True)
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
                yield Request(url= url,meta={"task":obj_tasks,"task_dir":mytask_dir}, callback=self.news)
                work_co += 4


            if task[0]['level'] == '3':
                temp = task[0]['url']
                work_co += 8
                yield Request(url=temp,meta={"task":obj_tasks,"task_dir":mytask_dir},callback=self.detail)
                #zk.delete(obj_tasks)




    def news(self, response):
        data = response.body.decode('GBK','ignore')
        titles = re.findall('{title : "(.*?)",id', data)
        urls = re.findall('},title : ".*?url : "(.*?)",type', data)
        length = len(titles)
        j = 0
        for i in range(length):
            msg = '[{"motian":"0", "url":"' + str(urls[i]) + '", "level":"3", "content":"0"}]'
            try:
                my_node=zk.create(response.meta["task_dir"] + "/task-", value = msg, sequence = True)
            except Exception,e:
                print "create: %s"% e
            print "create success"
            if j%3 == 0:
                pass #print "job is upload"
            else:
                print "yield"
                yield Request(url=urls[i],meta = {"item":titles[i], "task":my_node,"task_dir":response.meta["task_dir"]}, callback=self.detail)
            j += 1
        zk.delete(response.meta["task"])
        work_co -=4
        print "news"

    def detail(self, response):
        print "detail"
        item = SinanewsItem()
        item['title'] = response.xpath('//div[@class="page-header"]/h1/text()').extract()[0].encode('utf-8')
        item['url'] = response.url
        item['sort'] = response.meta["item"].encode('utf-8')
        data = response.xpath('//*[@id="artibody"]')
        item['news'] = data.xpath('string(.)').extract()[0]
        tags = jieba.analyse.extract_tags(item['news'],topK=topK)
        item['keywords'] = (','.join(tags))
        
        #print item['title']    
        #print item['sort']
        #print item['keywords']
        #print item['news']
        
        yield item
        zk.delete(response.meta["task"])
        work_co -=8