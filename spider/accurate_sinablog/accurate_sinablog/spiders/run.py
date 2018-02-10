#!/usr/bin/env python
# coding=utf-8

from scrapy import cmdline

cmdline.execute("scrapy crawl spider_accurate_sinablog -a keywords=坚果".split())

