# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import logging
from scrapy.exceptions import DropItem

class MongoPipeline(object):
    # collection_name = 'article_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.aids_seen = set()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        if hasattr(spider, 'collection_name'):
            self.collection_name = spider.collection_name

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if item['aid'] in self.aids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.aids_seen.add(item['aid'])
            self.db[self.collection_name].insert(dict(item))
            logging.debug("Article added to MongoDB")
            return item
