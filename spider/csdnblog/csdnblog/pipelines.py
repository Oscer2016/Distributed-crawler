# -*- coding: utf-8 -*-

# Define your item pipelines heremZ#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from pymongo import MongoClient

class CsdnblogPipeline(object):
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        mdb = self.client['csdnblog']
        self.collection = mdb['csdnblog']

    def process_item(self, item, spider):
        data = dict(item)
        self.collection.insert(data)
        
        return item

    def close_spider(self, spider):
        self.client.close()
