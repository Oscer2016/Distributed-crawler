#!/usr/bin/env python
# coding=utf-8

# Jack Kang
from kazoo.client import KazooClient
zk = KazooClient("123.206.89.123:2181")
zk.start()
if zk.exists("/task/taobao") != None:
    zk.delete('task/taobao',recursive = True)
if len(zk.get_children("/signal/taobao")) != 0:
    zk.delete("/signal/taobao", recursive = True);
    zk.create("/signal/taobao")
print "begin"

zk.create("/signal/taobao/start")
zk.stop()
