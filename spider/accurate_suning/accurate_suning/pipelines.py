# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

class AccurateSuningPipeline(object):
    
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        mdb = self.client['suning']
        self.collection = mdb['www.suning.com']

    def process_item(self, item, spider):
        data = dict(item)
        try:
            self.collection.insert(data)
        except Exception, e:
            print "Insert error: %s" % e

        return item
    
    def close_spider(self, spider):
        self.client.close()
