# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AccurateCnblogsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    title = scrapy.Field()
    releaseTime = scrapy.Field()
    url = scrapy.Field()
    sort = scrapy.Field()
    tags = scrapy.Field()
    readnum = scrapy.Field()
    article = scrapy.Field()
    keywords = scrapy.Field()

