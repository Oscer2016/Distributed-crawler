#!/usr/bin/env python
# -*- coding:utf-8 -*-

import threading
import SocketServer
import re
import json
import signal
import pymysql
import mysql.connector
import MySQLdb
from crawler import Crawler
from pymongo import MongoClient
from time import sleep
from kazoo.client import KazooClient
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#os.system("./clear.sh")

hosts_list =  ['123.206.89.123:2181', '123.207.157.135:2181', '118.89.234.46:2181']
zk = KazooClient(hosts = hosts_list)
zk.start()
#db = pymysql.connect(host="localhost",user="root",passwd="765885195",db="HP",charset="utf8")
#db = mysql.connector.connect(user="root", passwd="765885195", database="HP", use_unicode=True)
db = MySQLdb.connect("localhost", "root", "765885195", "HP")

instant_data = ["35"]

# 支持的网站信息
info = {'0':['www.taobao.com','1'],
        '1':['www.tmall.com','1'],
        '2':['www.jd.com','1'],
        '3':['www.suning.com','1'],
        '4':['www.gome.com','1'],
        '5':['www.amazon.cn','1'],
        '6':['www.dangdang.com','1'],
        '7':['www.cnblogs.com','2'],
        '8':['blog.csdn.net','2'],
        '9':['blog.sina.com.cn','2'],
        '10':['blog.51cto.com','2'],
        '11':['blog.hexun.com','2'],
        '12':['www.chinanews.com','3'],
        '13':['www.chinadaily.com.cn','3'],
        '14':['www.eastday.com','3'],
        '15':['www.huanqiu.com','3'],
        '16':['news.sina.com.cn','3'],
       }
info_zk = {'0':['taobao','1'],
        '1':['www.tmall.com','1'],
        '2':['jingdong','1'],
        '3':['suning','1'],
        '4':['gome','1'],
        '5':['amazon','1'],
        '6':['dangdang','1'],
        '7':['cnblog','2'],
        '8':['csdnblog','2'],
        '9':['sinablog','2'],
        '10':['ctoblog','2'],
        '11':['hexunblog','2'],
        '12':['chinanews','3'],
        '13':['chinadaily','3'],
        '14':['eastnews','3'],
        '15':['huanqiunews','3'],
        '16':['sinanews','3'],
       }       
state_map = {"5":"continue", "8":"pause", "13":"stop"}
node_map = {}

# MongoDB连接句柄
mdb = []

def Saveto_mysql():
    ip_list = []
    sql = "select * from info"
    try:
        cur = db.cursor()
        cur.execute(sql)
        db.commit()
        result = cur.fetchall()
        
        for field in result:
            mdb.append(str("%010d" % field[0]))
            ip_list.append(field[1])
        del result
        cur.close()
        print ip_list
    except Exception, e:
        print "Error: %s" % e

    num = len(mdb)

    for i in range(num):
        tip = ip_list[i].split('.')
        db_name = ""
        for t in tip:
            db_name += t
        ip_list[i] = MongoClient(ip_list[i], 27017)
        mdb.append(ip_list[i][db_name])

    while True:
        num = len(mdb)
        collections = {}
        tsql = "select * from task"
        try:
            cur = db.cursor()
            cur.execute(tsql)
            db.commit()
            result = cur.fetchall()
        
            for task in result:
                li = []
                li.append(task[1])
                li.append(task[2])
                collections[task[0]] = li
            del result
            cur.close()
        except Exception, e:
            print "HP said Error: %s" % e
            #sys.exit(0)
   
        print collections

        for coll in collections.keys():
            sum = 0
            coll_name = info[coll][0]
            keywords = collections[coll][0]
            genre = collections[coll][1]

            if not keywords:
                for i in range(num):
                    try:
                        sum += mdb[i][coll_name].count()
                    except Exception,e:
                        pass
            else:
                for i in range(num):
                    sum += mdb[i][keywords].count()
            str_sql = "insert into amount values('"+str(coll)+"', '"+str(keywords)+"', "+str(sum)+", '"+str(genre)+"', now())"
            print str_sql
            try:
                cur = db.cursor()
                cur.execute(str_sql)
                db.commit()
                result = cur.fetchall()
                del result
                cur.close()
            except Exception, e:
                print "Error: %s" % e
        sleep(10)

def drop_data(url, keywords):
    num = len(mdb)
    coll_name = info[url][0]
    if not keywords:
        for coll in mdb:
            coll[coll_name].remove({})
    else:
        for i in range(num):
            coll[keywords].remove({})


class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def get_ready_node(self, priority):
        ready_list = []
        for i in range(priority):
            task_num_max = 9999                           
            for node in node_map:
                if node_map[node][1] == '21' and node_map[node][2] < task_num_max and node not in ready_list:
                    obj_node = node
                    task_num_max = node_map[node][2]
            ready_list.append(obj_node)
        return ready_list

    def handle(self):
        print self.request.getpeername()
        while True:
            try:
                data = self.request.recv(1024)
                print data
                jdata = json.loads(data)
            except Exception, e:
                print "正在等待主控发来指令...."
                break
            

            # 请求正在运行任务
            #url+ '' ['1']
            if jdata[0]['Agreement'] == '1':
                print 'mt请求正在运行任务....'
                task = ['1']
                sql = "select * from task where status='5' or status='8'"
                print sql
                try:
                    cur = db.cursor()
                    cur.execute(sql)
                    db.commit()
                    result = cur.fetchall()
                    task.append(result[0][0])
                    task.append(result[0][1])
                    task.append(result[0][2])
                    # 将机器名用逗号连接起来
                    temp = []
                    for field in result:
                        temp.append('%010d' % field[3])
                    task.append(','.join(temp))
                    task.append(result[0][4].strftime("%Y-%m-%d %H:%M:%S"))
                    task.append(result[0][5])
                    print "$$$"
                    print  task
                    del result
                    cur.close()
                except Exception, e:
                    print "get working task SQL Error: %s" % e
                try:
                    print task
                    print json.dumps(task)
                    self.request.sendall(json.dumps(task))
                except Exception, e:
                    print "get working task Send error: %s" % e

            # 获取所有任务(li shi ren wu)
            # server 
            elif jdata[0]['Agreement'] == '2':
                print 'mt请求所有任务....'
                task = ['2']
                sql = "select * from task"
                print sql
                try:
                    cur = db.cursor()
                    cur.execute(sql)
                    db.commit()
                    result = cur.fetchall()

                    for field in result:
                        task.append(field[0])
                        task.append(field[1])

                    del result
                    cur.close()

                except Exception, e:
                    print "get all task SQL Error: %s" % e
                try:
                    print task
                    print json.dumps(task)
                    self.request.sendall(json.dumps(task))
                except Exception, e:
                    print "get all task Send error: %s" % e

            # 获取终止任务 
            # server
            elif jdata[0]['Agreement'] == '3':
                print 'mt请求所有任务....'
                task = ['3']
                sql = "select * from task where status='13'"
                print sql
                try:
                    cur = db.cursor()
                    cur.execute(sql)
                    db.commit()
                    result = cur.fetchall()

                    for field in result:
                        task.append(field[0])
                        task.append(field[2])
                    
                    del result
                    cur.close()

                except Exception, e:
                    print "get end task SQL Error: %s" % e
                try:
                    print task
                    print json.dumps(task)
                    self.request.sendall(json.dumps(task))
                except Exception, e:
                    print "get end task Send Error: %s" % e

            # 混合url任务请求
            # zk 
            elif jdata[0]['Agreement'] == '4':
                urls = jdata[0]['Content'].split(', ')
                print 'urls', urls
                priority = int(urls[len(urls)-1])
                for i in range(len(urls)-1):
                    url = str(urls[i])
                    task_type = info_zk[url][0]
                    ready_list = self.get_ready_node(priority)

                    for j in range(priority):
                        print ready_list[j] + "&&&"
                        zk.set("/command/" + ready_list[j], value = task_type)
                        node_map[ready_list[j]][2] += 1 # task_num++
                    temp_list = zk.get_children("/signal/" + task_type)
                    for i in temp_list:
                        zk.delete('/signal/' + task_type + '/' +str(i))
                    zk.create("/signal/" + task_type + '/start')
                    for ready_node in ready_list:
                        sql = "insert into task values('"+url+"','','"+info[url][1]+"',"+ready_node+",now(),'5')"
                        nsql = "update info set tasknum=tasknum+1 where id='" + ready_node + "'"
                        # 发布任务后在amount表中插入20条空数据，防止出现时间倒序
                        tsql = "insert into amount values('"+url+"','',0,'"+info[url][1]+"',now())"
                        for i in range(20):
                            try:
                                cur = db.cursor()
                                cur.execute(tsql)
                                db.commit()
                                result = cur.fetchall()
                                del result
                                cur.close()
                            except Exception, e:
                                print 'insert amount(indistinct) execute error: ', e
                        try:
                            cur = db.cursor()
                            cur.execute(sql)
                            cur.execute(nsql)
                            db.commit()
                            result = cur.fetchall()
                            del result
                            cur.close()
                        except Exception, e:
                            print "start task(multi) SQL Error: %s" % e
                    

                print priority
                print type(priority)
                try:
                    self.request.sendall(json.dumps(["4","0"]))
                except Exception, e:
                    self.request.sendall(json.dumps(["4","-1"]))
                    print "start task(multi) Send error: %s" % e
            
            # 发布精确任务
            # zk
            elif jdata[0]['Agreement'] == '5':
                urls = jdata[0]['Content'].split(', ')
                print 'urls', urls
                url = str(urls[0])
                keyword = urls[1]
                priority = int(urls[2])
                task_type = info_zk[url][1] + '_' + keyword

         
                ready_list = self.get_ready_node(priority)
                for i in range(priority):
                    zk.set("/command/" + ready_list[i], value = task_type)
                    node_map[ready_list[i]][2] += 1 # task_num++
                if zk.exists("/signal/" + task_type) != None:
                    temp_list = zk.get_children("/signal/" + task_type)
                    for i in temp_list:
                        zk.delete('/signal/' + task_type + '/' +str(i))
                else:
                    zk.create("/signal/" + task_type)
                    
                zk.create("/signal/" + task_type + '/start')
                for ready_node in ready_list:
                    sql = "insert into task values('"+url+"', '"+keyword+"','"+info[url][1]+"',"+int(ready_node)+",now(),'5')"
                    nsql = "update info set tasknum=tasknum+1 where id='" + ready_node + "'"
                    # 发布任务后在amount表中插入20条空数据，防止出现时间倒序
                    tsql = "insert into amount values('"+url+"','"+ keyword+"',0,'"+info[url][1]+"',now())"
                    for i in range(20):
                        try:
                            cur = db.cursor()
                            cur.execute(tsql)
                            db.commit()
                            result = cur.fetchall()
                            del result
                            cur.close()
                        except Exception, e:
                            print 'insert amount(accurate) execute error: ', e
                    try:
                        cur = db.cursor()
                        cur.execute(sql)
                        cur.execute(nsql)
                        db.commit()
                        result = cur.fetchall()
                        del result
                        cur.close()
                    except Exception, e:
                        print "start task(acc) SQL Error: %s" % e
                try:
                    self.request.sendall(json.dumps(["5","0"]))
                except Exception, e:
                    self.request.sendall(json.dumps(["5","-1"]))
                    print "start task(acc) Send error: %s" % e

            # 发布即时任务
            # no
            elif jdata[0]['Agreement'] == '8':
                del instant_data[:]
                instant_data.append('35')
                try:
                    self.request.sendall(json.dumps(["8","0"]))
                except Exception, e:
                    self.request.sendall(json.dumps(["8","-1"]))
                    print "start im task Send error: %s" % e
                try:
                    urls = jdata[0]['Content'].split(', ')
                    for url in urls:
                        if not url.startswith('http'):
                            url = "http://" + url
                        crawl = Crawler(url)
                        if re.search('taobao', url):
                            instant_data.append(url)
                            instant_data.append("1")
                            instant_data.append(str(crawl.spider_taobao()))
                        elif re.search('blog.sina', url):
                            instant_data.append(url)
                            instant_data.append("0")
                            instant_data.append(crawl.spider_sinablog())
                        elif re.search('blog.csdn', url):
                            instant_data.append(url)
                            instant_data.append("0")
                            instant_data.append(crawl.spider_csdnblog())
                        elif re.search('tmall', url):
                            instant_data.append(url)
                            instant_data.append("1")
                            instant_data.append(str(crawl.spider_tmall()))
                        elif re.search('jd.com', url):
                            instant_data.append(url)
                            instant_data.append("1")
                            instant_data.append(str(crawl.spider_jingdong()))
                        elif re.search('news.sina', url):
                            instant_data.append(url)
                            instant_data.append("0")
                            instant_data.append(crawl.spider_sinanews())
                        elif re.search('chinanews', url):
                            instant_data.append(url)
                            instant_data.append("0")
                            instant_data.append(crawl.spider_chinanews())

                    print instant_data
                except Exception, e:
                    print "start im task Error: %s" % e

            # 修改任务状态
            # pause continue stop
            # to do  : continue time 
            elif jdata[0]['Agreement'] == '9':
                obj_list = []
                data = jdata[0]['Content'].split(',')
                sql = "select id from task where url='" + data[0] + "' and keywords='" + data[1] + "'"
                print sql
                try:
                    cur = db.cursor()
                    cur.execute(sql)
                    db.commit()
                    result = cur.fetchall()

                    for field in result:
                        obj_list.append("%010d" % field[0])

                except Exception, e:
                    print "change task state SQL(select) Error: %s" % e
                task_state = state_map[str(data[2])]
                task_type =  info_zk[str(data[0])][0]
                task_keyword = str(data[1])

                if task_keyword != '':
                    task_type = task_type + '_' + task_keyword
                print task_type
                temp_list = zk.get_children("/signal/" + task_type)
                for i in temp_list:
                    zk.delete('/signal/' + task_type + '/' +str(i))

                zk.create('/signal/' + task_type + '/' + task_state)
                if task_state == "stop":
                    # sql = "update task set status='13' where url='" + data[0] + "' and keywords='" + data[1] + "'"
                    sql = "delete from task where url='" + data[0] + "' and keywords='" + data[1] + "'"

                    try:
                        cur = db.cursor()
                        cur.execute(sql)
                        db.commit()
                        result = cur.fetchall()
                        del result
                        cur.close()
                    except Exception, e:
                        print "change task state SQL(delete) Error: %s" % e

                    for obj_node in obj_list:
                        nsql = "update info set tasknum=tasknum-1 where id='" + obj_node + "'"
                        node_map[obj_node][2] -= 1
                    try:
                        cur = db.cursor()
                        cur.execute(nsql)
                        db.commit()
                        result = cur.fetchall()
                        del result
                        cur.close()
                    except Exception, e:
                        print "change task state SQL(tasknum--) Error: %s" % e

                sql = "update task set status = '"+str(data[2])+"' where url='"+str(data[0])+"' and keywords='" + str(data[1]) + "'"
                
                try:
                    cur = db.cursor()
                    cur.execute(sql)
                    db.commit()
                    result = cur.fetchall()
                    del result
                    cur.close()
                except Exception, e:
                    print "change task state SQL(update) Error: %s" % e
                try:
                    self.request.sendall(json.dumps(["9","0"]))
                except Exception, e:
                    self.request.sendall(json.dumps(["9","-1"]))
                    print "change task state Send error: %s" % e
            
            # 获取任务及下载总数
            # no
            elif jdata[0]['Agreement'] == '13':
                print 'mt请求任务及下载总数....'
                task = ['13']
                sql = "select url,keywords,max(total) from amount group by url,keywords"
                print sql
                try:
                    cur = db.cursor()
                    cur.execute(sql)
                    db.commit()
                    result = cur.fetchall()

                    for field in result:
                        task.append(field[0])
                        task.append(field[1])
                        task.append(field[2])

                    del result
                    cur.close()
                except Exception, e:
                    print "get task amount SQL Error: %s" % e
                try:
                    print task
                    print json.dumps(task)
                    self.request.sendall(json.dumps(task))
                except Exception, e:
                    print "get task amount Send error: %s" % e
            
            # 查看数据日志
            # no
            elif jdata[0]['Agreement'] == '21':
                print '正在查看数据日志'
                log = ['21']
                data = jdata[0]['Content'].split(', ')
                #tsql = "select count(1) from amount"
                #cur = db.cursor()
                #cur.execute(tsql)
                #num = cur.fetchall()[0][0]
                #if num < 10:
                #    sql = "select * from amount where url='" + str(data[0]) + "' and keywords='" + str(data[1]) + "'"
                #else:
                sql = "select * from amount where time in (select time from (select * from amount where url='"+str(data[0])+"' and keywords='"+str(data[1])+"' order by time desc limit 10) as tp)"
                print sql
                try:
                    cur = db.cursor()
                    cur.execute(sql)
                    db.commit()
                    result = cur.fetchall()

                    for field in result:
                        log.append(field[2])
                        #log.append(field[4].strftime("%m/%d %H:%M:%S"))
                        log.append(field[4].strftime("%H:%M:%S"))
                    print log
                    del result
                    cur.close()

                except Exception, e:
                    print "get log SQL Error: %s" % e
                try:
                    self.request.sendall(json.dumps(log))
                except Exception, e:
                    print "get log Send error: %s" % e
    
            # 获取任务下载总数
            # no
            elif jdata[0]['Agreement'] == '34':
                print 'mt请求历史任务下载总数....'
                task = ['34']
                esql = "select sum(total) from (select url,keywords,genre,max(total) as total from amount where genre='1' group by url,keywords,genre) as tp"
                bsql = "select sum(total) from (select url,keywords,genre,max(total) as total from amount where genre='2' group by url,keywords,genre) as tp"
                nsql = "select sum(total) from (select url,keywords,genre,max(total) as total from amount where genre='3' group by url,keywords,genre) as tp"
                
                print esql
                print bsql
                print nsql
                try:
                    cur = db.cursor()
                    cur.execute(esql)
                    db.commit()
                    result_esum = cur.fetchall()
                    cur.execute(bsql)
                    db.commit()
                    result_bsum = cur.fetchall()
                    cur.execute(nsql)
                    db.commit()
                    result_nsum = cur.fetchall()
                    if result_esum[0][0] is None:
                        task.append(0)
                    else:
                        task.append(int(result_esum[0][0]))
                    if result_bsum[0][0] is None:
                        task.append(0)
                    else:
                        task.append(int(result_bsum[0][0]))
                    if result_nsum[0][0] is None:
                        task.append(0)
                    else:
                        task.append(int(result_nsum[0][0]))

                    print task
                    del result_esum
                    del result_bsum
                    del result_nsum
                    cur.close()

                except Exception, e:
                    print "get down data sql Error: %s" % e
                try:
                    print task
                    print json.dumps(task)
                    self.request.sendall(json.dumps(task))
                except Exception, e:
                    print "get down data Send error: %s" % e
           
            # 发送即时任务数据
            elif jdata[0]['Agreement'] == '35':

                try:
                    if not instant_data:
                        self.request.sendall(json.dumps(['35']))
                    else:
                        self.request.sendall(json.dumps(instant_data))
                except Exception, e:
                    print "send im dataSend error: %s" % e
            

            elif jdata[0]['Agreement'] == '55':  # refresh node state
                print 'mt请求从机资源....'
                resource_info = ['55']

                for node in node_map:
                    if zk.exists("/command/" + node) != None:
                        node_map[node][1] = '21' # alive-working
                        sql = "update info set status='21' where id='" + node + "'"
                        try:
                            cur = db.cursor()
                            cur.execute(sql)
                            db.commit()
                            result = cur.fetchall()
                            del result
                            cur.close()
                        except Exception, e:
                            print "refresh node SQL Error: %s" % e
                    elif node_map[node][1] == '21':
                        node_map[node][1] = '34' # dead
                        sql = "update info set status='34' where id='" + node + "'"
                        tsql = "update info set tasknum=0 where id='" + node + "'"
                        try:
                            cur = db.cursor()
                            cur.execute(sql)
                            cur.execute(tsql)
                            db.commit()
                            result = cur.fetchall()
                            del result
                            cur.close()
                        except Exception, e:
                            print "refresh node SQL Error: %s" % e

                    resource_info.append(node)
                    resource_info.append(node_map[node][0])
                    resource_info.append(node_map[node][1])
                    resource_info.append(node_map[node][2])

                try:
                    print resource_info
                    print json.dumps(resource_info)
                    self.request.sendall(json.dumps(resource_info))
                except Exception, e:
                    print "refresh node Send error: %s" % e
           

            elif jdata[0]['Agreement'] == '56':  # change node state
                data = jdata[0]["Content"].split(',')
                tsql = "delete from task where id='" + data[1] + "'"
                sql = "update info set status = '" + data[1] + "' where id = '" + data[0] + "'"
                if data[1] == '55':              # stop a node
                    zk.set("/command/" + data[0], value = "stop")
                    zk.delete("/command/" + data[0])
                    node_map[data[0]][1] = '34'  # node is over
                else:                            # start a node
                    obj_ip = node_map[data[0]][0]
                    print "^^^^" + data[0]
                    cmd = "ssh root@{} 'python /root/V3/project/run.py {} 1>log' &".format(obj_ip, "%010d" % int(data[0]))
                    os.system(cmd)
                    node_map[data[0]][1] = '21'  # node is working 
                try:
                    cur = db.cursor()
                    cur.execute(sql)
                    cur.execute(tsql)
                    db.commit()
                    result = cur.fetchall()
                    del result
                    cur.close()
                except Exception, e:
                    print "Change node state: %s" % e
   
                try:
                    self.request.sendall(json.dumps(["56","0"]))
                except Exception, e:
                    self.request.sendall(json.dumps(["56","-1"]))
                    print "Change node Send error: %s" % e
            

            elif jdata[0]['Agreement'] == '57': # delete / add a node 
                data = jdata[0]["Content"].split(',')
                ip = data[1]
                

                if data[0] == "0":              # delete a node
                    sql = "delete from info where id = '" + data[1] + "'"
                    # tsql = "update task set status='13' where id='" + data[1] + "'"

                    node_map.pop(data[1])
                    try:
                        cur = db.cursor()
                        cur.execute(sql)
                        #cur.execute(tsql)
                        db.commit()
                        result = cur.fetchall()
                        del result
                        cur.close()

                    except Exception, e:
                        print "delete SQL Error: %s" % e
                elif data[0] == "1": 
                    # 将MongoDB连接句柄追加到全局列表中
                    tip = ip.split('.')
                    db_name = ""
                    for t in tip:
                        db_name += t
                    client = MongoClient(ip, 27017)
                    mdb.append(client[db_name])
                    
                    sql = "insert into info values(null,'" + data[1] + "','55',0)"
                    try:
                        cur = db.cursor()
                        cur.execute(sql)
                        db.commit()
                        result = cur.fetchall()
                        del result
                        cur.close()
                    except Exception, e:
                        print "add SQL Error: %s" % e

                    tsql = "select max(id) from info"
                    try:
                        cur = db.cursor()
                        cur.execute(tsql)
                        db.commit()
                        result = cur.fetchall()
                        cur.close()
                    except Exception, e:
                        print "add-query node: %s" % e
                    
                    node_name = "%010d" % result[0][0]
                    node_map[node_name] = list((ip, '55', 0)) 
                    del result
                

                try:
                    self.request.sendall(json.dumps(["57","0"]))
                except Exception, e:
                    self.request.sendall(json.dumps(["57","-1"]))
                    print "add / delete Send error: %s" % e

            # 删除数据
            # no
            elif jdata[0]['Agreement'] == '89':
                data = jdata[0]["Content"].split(',')
                sql = "delete from amount where url='"+data[0]+"' and keywords='"+data[1]+"'"
                try:
                    cur = db.cursor()
                    cur.execute(sql)
                    db.commit()
                    result = cur.fetchall()
                    del result
                    cur.close()
                except Exception, e:
                    print "delete data SQL Error: %s" % e

                
                # 删除Mongodb数据
                mt = threading.Thread(target=drop_data,args=(data[0], data[1]))
                mt.start()

                try:
                    self.request.sendall(json.dumps(["89","0"]))
                except Exception, e:
                    self.request.sendall(json.dumps(["89","-1"]))
                    print "delete data Send error: %s" % e

def sigint_handler(signum, frame):
    print 'catched interrupt signal!'

def mysql_to_memory():
    sql = "select * from info"
    try:
        cur = db.cursor()
        cur.execute(sql)
        db.commit()
        result = cur.fetchall()
        for field in result:
            node_map["%010d" % field[0]] = list((field[1], field[2], field[3]))
        del result
        cur.close()
    except Exception, e:
        print "mysql_to_memory SQL Error: %s" % e   

if __name__ == "__main__":
    

    signal.signal(signal.SIGINT, sigint_handler)

    mysql_to_memory()
    
    HOST, PORT = "172.18.214.188", 8888
    
    SocketServer.TCPServer.allow_reuse_address = True
    server = SocketServer.ThreadingTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)

    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print "Server loop running in thread:", server_thread.name
    print "waiting for connection....."

    # save data num to mysql
    t = threading.Thread(target=Saveto_mysql,args=())
    t.start()
 
    server.serve_forever()

