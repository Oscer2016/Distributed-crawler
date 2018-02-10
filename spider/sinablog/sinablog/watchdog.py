# -*- coding: utf-8 -*-

from kazoo.client import KazooClient
import os
import sys
import logging
import time
import signal
from multiprocessing import Process

main_dir = "/home/kang/Distributed-crawler/project/"
signal_dir = '/signal/sinablog'
task_type = "sinablog"
def run_proc():
    os.chdir(main_dir +"sinablog/sinablog/spiders")
    #arg = ["HELLO","crawl", "spider_" + task_type,"--nolog"]
    arg = ["HELLO","crawl", "spider_" + task_type]
    os.execvp("scrapy",arg)


watchPid = [] 
for i in range(1,len(sys.argv)):
    watchPid.append(int(sys.argv[i]))

hosts_list =  ['123.206.89.123:2181', '123.207.157.135:2181', '118.89.234.46:2181']
signal_dic = {"stop":signal.SIGKILL, "start":signal.SIGCONT, "pause":signal.SIGSTOP, "continue":signal.SIGCONT}
zk = KazooClient(hosts = hosts_list)
logging.basicConfig()
zk.start()
print "watch dog working"

@zk.ChildrenWatch(signal_dir)
def signal_watch(children):
    if len(children) != 0:
        print children[0]
        global watchPid
        for pid in watchPid:
            os.kill(pid, signal_dic[children[0]])
        #zk.delete(signal_dir+ '/' + children[0])
def check(pid):
    try:
     	os.kill(pid, 0) 
     	return pid
    except Exception:  #判断
        p = Process(target=run_proc)
        p.start()
        return p.pid
    	
while True:
    print "begin check"
    for pid in watchPid:
        newpid = check(pid)
        if newpid != pid:
        	print "new process"
        	watchPid.remove(pid)
        	watchPid.append(newpid)
    #try:
    #    os.waitpid(-1, 0)
    #except Exception,e:
    #    print "no child"
    #print "end check"
    time.sleep(5)

