# -*- coding: utf-8 -*-

# Scrapy settings for tmall project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'tmall'

SPIDER_MODULES = ['tmall.spiders']
NEWSPIDER_MODULE = 'tmall.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1.5
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
    'cookie': 'thw=cn; miid=1877326715353705246; ctoken=0P0JvKEIyk15qEwpK8LIiceland; tk_trace=oTRxOWSBNwn9dPyscxqAz9fIO73QQFhF7kVkgTL59JVC7kpGpQEdOb67caDmPjbIYxYMRUFXKcCXX%2FfQ1h8gXuGVrgjD61F%2B0DFnRC5EMB7aZ9NOo63GAUmnCjjrIY5wkGyucBWS44YHI4A6d%2BLNSACICaG8KC2tFYpVmX%2BjxKj4tEcAteNhxHEPvOhSJbYqgm9OvDy9VPmorkl1GZEBZo8OvIgVoPbrrTrCdOyH18y6BkHGva4kbB8xuQw62sSLb2eyt8bjx62%2B1sUCi8z0z2oWb26s6hziPr0T5GVnMnPDD%2Bmuyr6pAHiyPPI4OKTerpb3ea5uGXy8TcrjbxvIiQldLj5pLEUsZu8%3D; UM_distinctid=15e22e6bc6e1-0c5735b42741ab-3976045e-100200-15e22e6bc6f435; _m_h5_tk=8c383678bc2922e1521fbd203debdbaf_1503827636199; _m_h5_tk_enc=df906285a00b4f52fbc6c9fe8d3bc421; hng=CN%7Czh-CN%7CCNY%7C156; v=0; uss=BqeJtzLVJrTsSJ6X2LDYRdaWQ%2BKUXOOY8l7NE73sSoPSShTwCqvcl%2FyDvA%3D%3D; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; _tb_token_=533b3393509e0; whl=-1%260%260%261503930679329; cna=jiIfEsNey0MCAXUg2C6F55ir; uc1=cookie14=UoTcDNNnZUea6w%3D%3D&lng=zh_CN&cookie16=URm48syIJ1yk0MX2J7mAAEhTuw%3D%3D&existShop=false&cookie21=V32FPkk%2Fgipm&tag=8&cookie15=VFC%2FuZ9ayeYq2g%3D%3D&pas=0; uc3=sg2=VypZNAKKWWqEaSKA1GpGs%2B8tysrnwEF9TzJHu9Fo6tw%3D&nk2=F5RDKmmBskqoP%2BFa&id2=UU27LTb95wEmtQ%3D%3D&vt3=F8dBzWYdKC42Yr%2BbE1E%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D; existShop=MTUwMzk3MzcwNg%3D%3D; lgc=tb6668866688; tracknick=tb6668866688; cookie2=1055c0500c661fa5398031aa3bd27f5c; sg=897; mt=np=&ci=115_1&cyk=2_0; cookie1=B0eg4Md2wVeUEGrrbnYlnTqeCodw3QYsxMUcV2cWzeY%3D; unb=2592924029; skt=c0e93da15ffb6fec; t=f24179ca58a99063c6f1feabcbc17b12; _cc_=V32FPkk%2Fhw%3D%3D; tg=0; _l_g_=Ug%3D%3D; _nk_=tb6668866688; cookie17=UU27LTb95wEmtQ%3D%3D; isg=Ai8v8hTwqgLcE64Dpfv1gA-vvkr5fJ1c2I7spUG8dB6lkE2SSaUrRjUAZLZV; linezing_session=QJXBwjEeb4zxNhS670MXjI85_1503973736042rHlv_10',
    'user-agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'tmall.middlewares.TmallSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 751,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': None,
    #'tmall.middlewares.ProxyMiddleware': 750,
    'tmall.middlewares.UseragentMiddleware': 400,
    'tmall.middlewares.RetryMiddleware': 300,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'tmall.pipelines.TmallPipeline': 300,
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
