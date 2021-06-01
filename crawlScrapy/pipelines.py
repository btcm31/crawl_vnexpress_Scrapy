# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter

class CrawlscrapyPipeline:
    def process_item(self, item, spider):
        return item
    def open_spider(self, spider):
        self.csvfile  = open(self.filename, 'wb')
        self.exporter = CsvItemExporter(self.csvfile, encoding='utf-8')
        self.exporter.start_exporting()
