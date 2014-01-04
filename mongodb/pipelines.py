#! /usr/bin/python
#! -*- coding: utf-8 -*-
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter
from scrapy.exceptions import DropItem

import time

# 3rd party modules
import pymongo
 
from scrapy import log
from scrapy.conf import settings
from pymongo import MongoClient
 
class MongoDBPipeline(object):
    def __init__(self):
        #self.client = pymongo.MongoClient(settings['MONGODB_CONN'])
        self.db = pymongo.MongoClient(settings['MONGODB_CONN'])['scrapy']
        self.scrapy_products = self.db['scrapy_products']
        self.scrapy_categories = self.db['scrapy_categories']
        
    def process_item(self, item, spider):
        #err_msg = ''
        #for field, data in item.items():
        #    if not data:
        #        err_msg += 'Missing %s of poem from %s\n' % (field, item['urls'])
        #if err_msg:
        #    raise DropItem(err_msg)
        #self.scrapy_products.insert({'a':123,'b':321})
        if "MongodbItemCategory" in type(item).__name__:
            self.scrapy_categories.insert(dict(item))
        else:
            self.scrapy_products.insert(dict(item))
        #log.msg('Item written to scrapy_products %s/%s' % (self.db, self.scrapy_products),level=log.DEBUG, spider=spider)
        return item

class CsvExportPipeline(object):

    def __init__(self):
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.files = {}

    def spider_opened(self, spider):
        #file = open('%s_%s.csv' % (spider.name, int(time.time())), 'w+b')
        file_cat = open('%s_category.csv' % (spider.name), 'w+b')
        file_pro = open('%s_products.csv' % (spider.name), 'w+b')
        self.files[spider] = {file_cat,file_pro}
        self.exporter_cat = CsvItemExporter(file_cat,fields_to_export = ['sourceid','source','urls','createddatetime','name','description','productlinks','imagelinks'])
        self.exporter_pro = CsvItemExporter(file_pro,fields_to_export = ['sourceid','source','urls','createddatetime','name','onstock','mainimage','otherimages','shortdescription','description','details','relatedlinks','upselllinks','price','specialprice','currency'])
        self.exporter_cat.start_exporting()
        self.exporter_pro.start_exporting()

    def spider_closed(self, spider):
        self.exporter_cat.finish_exporting()
        self.exporter_pro.finish_exporting()
        file_cat = self.files.pop(spider)
        file_pro = self.files.pop(spider)
        file_cat.close()
        file_pro.close()

    def process_item(self, item, spider):
        if item is None:
            raise DropItem("None")
        log.msg('*** type is ' + str(type(item).__name__),                level=log.DEBUG, spider=spider)
        if "MongodbItemCategory" in type(item).__name__:
            self.exporter_cat.export_item(item)
        else:
            self.exporter_pro.export_item(item)
        return item 
