# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient


class SuningPipeline(object):

    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        mdb = self.client['suning']
        self.collection = mdb['suning']

    def process_item(self, item, spider):
        title = item['title']
        link = item['link']
        price = str(item['price'])
        print price
        print title
        data = dict(item)

        try:
            self.collection.insert(data)
        except Exception, e:
            print "Insert error: %s" % e

        return item
