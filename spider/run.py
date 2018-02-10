#!/usr/bin/env python
# coding=utf-8

from scrapy import cmdline
import os
import sys
from kazoo.client import KazooClient
import time
from multiprocessing import Process
from random import randint
import logging

def launcher(arg):
    os.execvp("python",arg)
if __name__ == '__main__':
    logging.basicConfig()
    hosts_list =  ['123.206.89.123:2181', '123.207.157.135:2181', '118.89.234.46:2181']
    zk  = KazooClient(hosts = hosts_list)
    zk.start()

    command_dir = "/command/"
    my_node =zk.create(command_dir + "computer-", sequence = True, ephemeral = True, value = "empty")
    
    @zk.DataWatch(my_node)
    def command_watch(data, stat):  
        task_type = data
        print task_type
        if task_type != "empty":
            arg = ["hello","launcher.py",task_type,str(3)]
            task = Process(target = launcher, args = (arg, ))
            task.start()
            zk.set(my_node, value = "empty")


    time.sleep(1000)
