# -*- coding: utf-8 -*-

from kazoo.client import KazooClient
import os
import sys
import logging
import time
import signal

signal_dir = '/signal/jingdong'


watchPid = [] # watching pid list 
for i in range(1,len(sys.argv)):
    watchPid.append(int(sys.argv[i]))
#for i in watchPid:
#    os.kill(i, signal.SIGSTOP)
hosts_list =  ['123.206.89.123:2181', '123.207.157.135:2181', '118.89.234.46:2181']
signal_dic = {"stop":signal.SIGKILL, "start":signal.SIGCONT, "pause":signal.SIGSTOP, "continue":signal.SIGCONT}
zk = KazooClient(hosts = hosts_list)
logging.basicConfig()
zk.start()
print "watch dog working"
#setWatchEvent()

@zk.ChildrenWatch(signal_dir)
def signal_watch(children):
	if len(children) != 0:
		print children[0]
		global watchPid
		for pid in watchPid:
			os.kill(pid, signal_dic[children[0]])
                print signal_dic[children[0]]
                zk.delete(signal_dir+ '/' + children[0])

time.sleep(50000)
