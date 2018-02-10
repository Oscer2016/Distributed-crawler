# -*- coding: utf-8 -*-

import scrapy
import jieba
import jieba.analyse
from optparse import OptionParser
from docopt import docopt
from scrapy import Request
from chinadaily.items import ChinadailyItem
from kazoo.client import KazooClient
#import logging

topK = 2


task_dir = '/task/chinadaily/'
hosts_list =  ['123.206.89.123:2181', '123.207.157.135:2181', '118.89.234.46:2181']
work_co = 0
working_list = []
zk = KazooClient(hosts = hosts_list)
#logging.basicConfig()

class SpiderChinadailySpider(scrapy.Spider):
    name = 'spider_chinadaily'
    allowed_domains = ['chinadaily.com.cn']
    start_urls = ['http://chinadaily.com.cn/']

    def parse(self, response):

        zk.start()
        #print "zk start"
        zode_path =  zk.create("/pid/chinadaily/node-" , ephemeral = True, sequence = True)
        myid = zode_path[-10 : ]
        mytask_dir = task_dir + "node-" + myid
        #print "geting lock"
        try:
            zk.create('/task/chinadaily')
            Master = True
        except :
            Master = False

        if Master == True:
            zk.create(mytask_dir)
            sleep(3)
            themes = response.xpath('//ul[@class="dropdown"]/li/a/@href').extract()
            nodes = len(zk.get_children("/pid/chinadaily"))
            real_nodes = zk.get_children("/task/chinadaily")
            print "realnodes" + str(real_nodes)
            while nodes != len(real_nodes):
                real_nodes = zk.get_children("/task/chinadaily")
                nodes = len(zk.get_children("/pid/chinadaily"))
                sleep(0.01)
             
            peer_tasks = len(themes) / nodes
            print "master is " + str(os.getpid())
            i = 0
            while i < nodes:
                j = 0
                while j < peer_tasks:
                    msg = '[{"motian":"0", "url":"' + str(themes[i*peer_tasks+j]) + '", "level":"2", "content":"0","state":"free"}]'
                    #print msg
                    zk.create("/task/chinadaily/" + real_nodes[i] + "/task-", value = msg, sequence = True)
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


            #print mytask_dir + "**"
            #print "parse  " + str(os.getpid()) + ' '+ task[0]['level'] + task[0]['url']
            if task[0]['level'] == '2':
                temp = task[0]['url']
                work_co += 1
                yield Request(url='http:' + temp[len(temp)-1],meta={"task":obj_tasks,"task_dir":mytask_dir},callback=self.sort)


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
        sorts = response.xpath('//div[@class="bt1"]/b/a/@href').extract()
        genres = response.xpath('//div[@class="bt1"]/b/a/text()').extract()
        length = len(sorts)
        j = 0
        for i in range(length):
            msg = '[{"motian":"0", "url":"' + response.url+sorts[i] + '", "level":"3", "content":"0"}]'
            #print msg
            my_node=zk.create(response.meta["task_dir"] + "/task-", value = msg, sequence = True)
            if j%3 == 0:
                pass #print "job is upload"
            else:
                yield Request(url=purl,meta = {"item":genres[i],"task":my_node,"task_dir":response.meta["task_dir"]}, callback=self.pageturning)
            j += 1
            

        zk.delete(response.meta["task"])
        work_co -= 1

    def pageturning(self, response):
        genre = response.meta["item"]
        if response.url.endswith('html'):
            yield Request(url=response.url+'?', meta={"item":genre}, callback=self.news)
            j = 0
            for i in range(100):
                url = response.url[:-5] + '{}.html'.format(str(i+2))
                msg = '[{"motian":"0", "url":"' + url + '", "level":"4", "content":"0"}]'
                #print msg
                my_node=zk.create(response.meta["task_dir"] + "/task-", value = msg, sequence = True)
                if j%3 == 0:
                    pass #print "job is upload"
                else:
                    yield Request(url=url,meta = {"item":genre,"task":my_node,"task_dir":response.meta["task_dir"]}, callback=self.news)
                j += 1
                
        else:
            yield Request(url=response.url+'index.html', meta={"item":genre}, callback=self.news)
            for i in range(100):
                url = response.url + 'index_{}.html'.format(str(i+2))
                msg = '[{"motian":"0", "url":"' + url + '", "level":"4", "content":"0"}]'
                #print msg
                my_node=zk.create(response.meta["task_dir"] + "/task-", value = msg, sequence = True)
                if j%3 == 0:
                    pass #print "job is upload"
                else:
                    yield Request(url=url,meta = {"item":genre,"task":my_node,"task_dir":response.meta["task_dir"]}, callback=self.news)
                j += 1


        zk.delete(response.meta["task"])
        work_co -= 2

    def news(self, response):
        genre = response.meta["item"]
        turl = '/'.join(response.url.split('/')[:-1]) + '/'
        data = response.xpath('//span/h4/a/@href').extract()
        i = 0
        for postfix in data:
            url = turl + postfix
            msg = '[{"motian":"0", "url":"' + url + '", "level":"5", "content":"0"}]'
            #print msg
            my_node=zk.create(response.meta["task_dir"] + "/task-", value = msg, sequence = True)
            if i%3 == 0:
                pass #print "job is upload"
            else:
                yield Request(url=url,meta = {"item":genre,"task":my_node,"task_dir":response.meta["task_dir"]},callback=self.detail)
            i += 1


        zk.delete(response.meta["task"])
        work_co -= 4
    
    def detail(self, response):
        #print response.url
        item = ChinadailyItem()

        item['title'] = response.xpath('//div/h1/text()').extract()[0].encode('utf-8')
        item['url'] = response.url
        item['sort'] = response.meta["item"]
        data = response.xpath('//div[@id="Content"]')
        item['news'] = data.xpath('string(.)').extract()[0]
        
        tags = jieba.analyse.extract_tags(item['news'],topK=topK)
        item['keywords'] = (','.join(tags))

        print item['title']
        #print item['url']
        print item['sort']
        #print item['news']
        print item['keywords']

        yield item
        zk.delete(response.meta["task"])
        work_co -= 8
