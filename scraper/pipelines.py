# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo


class ScraperPipeline:
    def process_item(self, item, spider):
        return item


class MongoPipeline:

    def __init__(self, mongo_uri, mongo_db, mongo_collection, primary_key):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collecion = mongo_collection
        self.primary_key = primary_key
        self.client = None
        self.db = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items'),
            mongo_collection=crawler.settings.get('MONGO_COLLECTION'),
            primary_key=crawler.settings.get('PRIMARY_KEY')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.mongo_collecion].update_one(
            {self.primary_key: item[self.primary_key]},
            {'$set': dict(item)},
            upsert=True
        )
        return item

