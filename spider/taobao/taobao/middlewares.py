# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import json 
import redis 
import random 
import base64
from scrapy import signals
from settings import USER_AGENTS, IPPOOL
from scrapy.downloadermiddlewares.retry import RetryMiddleware         # 重试中间件
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware # UserAegent中间件
from scrapy.contrib.downloadermiddleware.httpproxy import httpProxyMiddleware
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware

class IPPOOLS(httpProxyMiddleware):
    # 初始化
    def __init__(self, ip=''):
        self.ip=ip

    # 进行请求处理
    def process_request(self, request, spider):
        thisip = random.choice(IPPOOL)
        print "当前使用的IP是: " + thisip["ipaddr"]
        # 将对应的IP添加为具体的代理，用该IP进行爬取
        request.meta["proxy"]="http://"+thisip["ipaddr"]

class UserAgentMiddleware(UserAgentMiddleware):

    #def process_request(self, request, spider):
        #agent = random.choice(agents)
        #request.headers["User-Agent"] = agent
    """Randomly rotate user agents based on a list of predefined ones"""
    def __init__(self, agents = ''):
	self.agents = agents
    @classmethod
    def from_crawler(cls, crawler):
	return cls(crawler.settings.getlist('USER_AGENTS'))
    def process_request(self, request, spider):
	thisagents = random.choice(USER_AGENTS)
        print "Agents: " + thisagents
	request.headers.setdefault('User-Agent', thisagents)

class ProxyMiddleware(object):
    def process_request(self, request, spider):
	proxy = random.choice(PROXIES)
	if proxy['user_pass'] is not None:
	    request.meta['proxy'] = "http://%s" % proxy['ip_port']
	    encoded_user_pass = base64.encodestring(proxy['user_pass'])
	    request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
	    print "**************ProxyMiddleware have pass************" + proxy['ip_port']
	else:
	    print "**************ProxyMiddleware no pass************" + proxy['ip_port']
	    request.meta['proxy'] = "http://%s" % proxy['ip_port']
			       
class TaobaoSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
