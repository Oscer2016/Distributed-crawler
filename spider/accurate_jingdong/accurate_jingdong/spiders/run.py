#!/usr/bin/env python
# coding=utf-8

from scrapy import cmdline
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

cmdline.execute("scrapy crawl spider_accurate_jingdong -a keywords=坚果 --nolog".split())
