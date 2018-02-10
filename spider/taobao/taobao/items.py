# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class TaobaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    commentdata = scrapy.Field()
    shop = scrapy.Field()
    shopLink = scrapy.Field()
    describeScore = scrapy.Field()
    serviceScore = scrapy.Field()
    logisticsScore = scrapy.Field()
    #comment = scrapy.Field()
