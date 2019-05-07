# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import CsvItemExporter
from datetime import datetime

class WriteItemPipeline(object):

    def __init__(self):
        
        # now = datetime.strftime(datetime.now(), '%Y-%m-%d_%H:%M:%S')
        # with open("file.dat","a+") as f:
        # filename = 'kicktraq_' + now + '.csv'
        self.filename = 'kicktraq_final.csv' #do not forget to change the file name with smth like _date #filename

    def open_spider(self, spider):
        self.csvfile = open(self.filename, 'wb')
        self.exporter = CsvItemExporter(self.csvfile)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.csvfile.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item