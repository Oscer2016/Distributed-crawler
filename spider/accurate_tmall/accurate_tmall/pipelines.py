# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

class AccurateTmallPipeline(object):

    def __init__(self):
        self.client = MongoClient('localhost',27017)
        mdb = self.client['accurate_tamll']
        self.collection = mdb['accurate_tmall']

    def process_item(self, item, spider):
        data = dict(item)
        self.collection.insert(data)

        return item

    def close_spider(self, spider):
        self.client.close()

