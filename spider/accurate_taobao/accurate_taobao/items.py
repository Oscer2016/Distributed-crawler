# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class AccurateTaobaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    keywords = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    comment_data = scrapy.Field()
    shop_name = scrapy.Field()
    shop_link = scrapy.Field()
    describe_score = scrapy.Field()
    service_score = scrapy.Field()
    logistics_score = scrapy.Field()
    #comment = scrapy.Field()
