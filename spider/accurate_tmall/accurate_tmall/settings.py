# -*- coding: utf-8 -*-

# Scrapy settings for accurate_tmall project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'accurate_tmall'

SPIDER_MODULES = ['accurate_tmall.spiders']
NEWSPIDER_MODULE = 'accurate_tmall.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'accurate_tmall (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'referer': 'https://list.tmall.com/',
    'user-agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'cookie': 'cna=ky6NElQuFmACAXUg2BodChWA; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; v=0; _tb_token_=5eda7134b5bfb; miid=575914327324234604; tk_trace=oTRxOWSBNwn9dPy4KVJVbutfzK5InlkjwbWpxHegXyGxPdWTLVRjn23RuZzZtB1ZgD6Khe0jl%2BAoo68rryovRBE2Yp933GccTPwH%2FTbWVnqEfudSt0ozZPG%2BkA1iKeVv2L5C1tkul3c1pEAfoOzBoBsNsJySRlZDTaqUvcmOeTSfbPhej9x%2F2LthzVTJdNw4adByusK5vzhDBb%2FvOVBBomlI%2F4qcw9X39QbRNwRx3vmqbRxNKOgQmbDVlgMozJHVh%2F1YV3yP0MyAO3MnQ4USGENtqALydcC2BxdwLCi9UacpFPO6M8JyuOeAhM46X01YcHTtaipuk4uqDBn%2BtzA%3D; uc3=nk2=F5RDKmmBskqoP%2BFa&id2=UU27LTb95wEmtQ%3D%3D&vt3=F8dBzLQKZIXdBjZ36EU%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D; existShop=MTUxMjM4OTcxNA%3D%3D; lgc=tb6668866688; tracknick=tb6668866688; cookie2=2c0b92f6900de2376b790cd63db76f29; sg=897; cookie1=B0eg4Md2wVeUEGrrbnYlnTqeCodw3QYsxMUcV2cWzeY%3D; unb=2592924029; skt=c96676242fca22ae; t=7e6d3d1b42fb018f0fe0e19383430960; _cc_=URm48syIZQ%3D%3D; tg=0; _l_g_=Ug%3D%3D; _nk_=tb6668866688; cookie17=UU27LTb95wEmtQ%3D%3D; uc1=cookie16=V32FPkk%2FxXMk5UvIbNtImtMfJQ%3D%3D&cookie21=U%2BGCWk%2F7pY%2FF&cookie15=V32FPkk%2Fw0dUvg%3D%3D&existShop=false&pas=0&cookie14=UoTdeYfCsXRK7A%3D%3D&tag=8&lng=zh_CN; mt=ci=93_1; isg=AtfX-l1QQQtJfsWkXUoYx_9yZkLhtLUb28oKHykEwqYNWPeaMew7zpV4zs49'
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'accurate_tmall.middlewares.AccurateTmallSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 751,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': None,
    #'accurate_tmall.middlewares.ProxyMiddleware': 750,
    #'accurate_tmall.middlewares.UseragentMiddleware': 400,
    'accurate_tmall.middlewares.RetryMiddleware': 300,

}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'accurate_tmall.pipelines.AccurateTmallPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
