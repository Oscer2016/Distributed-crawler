# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
from scrapy import signals
from accurate_tmall.ippool import IPPOOL
from accurate_tmall.uapool import UAPOOL
from scrapy.contrib.downloadermiddleware.retry import RetryMiddleware
from scrapy.core.downloader.handlers.http11 import TunnelError
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware


class ProxyMiddleware(object):
    def __init__(self, ip = ''):
        self.ip = ip

    def process_request(self, request, spider):
        thisip = random.choice(IPPOOL)
        print "Current ip: " + thisip["ipaddr"]
        request.meta["proxy"] = "http://" + thisip["ipaddr"]


class UseragentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent = ''):
        self.user_agent = user_agent
    def process_request(self, request, spider):
        thisua = random.choice(UAPOOL)
        #print "Current useragent: " + thisua
        request.headers.setdefault('User-Agent', thisua)


class RetryMiddleware(RetryMiddleware):
    def process_exception(self, request, exception, spider):
        if ( isinstance(exception, self.EXCEPTIONS_TO_RETRY) or isinstance(exception, TunnelError) ) \
                and 'dont_retry' not in request.meta:
            return self._retry(request, exception, spider)
