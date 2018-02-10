#!/usr/bin/env python
# coding=utf-8

import re
from crawler import Crawler
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

url = raw_input('请输入url: ')

if url.startswith('http'):
    pass
else:
    url = 'http://' + url

crawl = Crawler(url)
a = []
if re.search('taobao', url):
    a.append(str(crawl.spider_taobao()))
elif re.search('tmall', url):
    a.append(str(crawl.spider_tmall()))
elif re.search('jd.com', url):
    a.append(str(crawl.spider_jingdong()))
elif re.search('blog.sina', url):
    a.append(str(crawl.spider_sinablog()))
elif re.search('blog.csdn', url):
    a.append(str(crawl.spider_csdnblog()))

print a

