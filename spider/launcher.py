# -*- coding: utf-8 -*-

from scrapy import cmdline
import os
import sys
from kazoo.client import KazooClient
import time
from multiprocessing import Process
from random import randint

main_dir = "/home/kang/Distributed-crawler/project/"
def run_dog(pid_list,task_type):
    os.chdir(main_dir + task_type + '/' + task_type)
    arg = ["HELLO","watchdog.py"]
    for pid in pid_list:
        arg.append(str(pid))
    print arg
    os.execvp("python",arg)

def run_proc(num, task_type):
    os.chdir(main_dir + task_type +'/' + task_type + "/spiders")
    #arg = ["HELLO","crawl", "spider_" + task_type,"--nolog"]
    arg = ["HELLO","crawl", "spider_" + task_type]
    os.execvp("scrapy",arg)
def run_blancer(task_type):
    os.chdir(main_dir + task_type +'/' + task_type )
    arg = ["HELLO","load_blancer.py"]
    os.execvp("python",arg)

hosts_list =  ['123.206.89.123:2181', '123.207.157.135:2181', '118.89.234.46:2181']
zk  = KazooClient(hosts = hosts_list)
zk.start()
task_type = sys.argv[1]
process_num = int(sys.argv[2])
print task_type
print process_num
signal_dir = "/signal/" + task_type
pid_list = []

@zk.ChildrenWatch(signal_dir)
def signal_watch(children):
    if len(children) != 0 and children[0] == 'start':
        for i in range(process_num):
            p = Process(target=run_proc, args=(str(i),task_type))
            p.start()
            #time.sleep(1) # to do : Master election
            pid_list.append(str(p.pid))
            #os.waitpid(p.pid, os.WNOHANG)
            #print p.pid
        #zk.delete(signal_dir + '/start')
        print pid_list
        dog = Process(target = run_dog, args =(pid_list, task_type))
        dog.start()
        #load_blancer = Process(target = run_blancer, args = (task_type, ))
        #load_blancer.start()
        for i in pid_list:
            pid_list.remove(i)
while True:
    try:
        os.waitpid(-1, 0)
    except Exception,e:
        print "no child"
    time.sleep(1)
time.sleep(1000)
