# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
from .items import CountryPopulationItem, HistoricalPopulationItem, ForecastPopulationItem, CitiesPoulation


class ScraperPipeline:
    def process_item(self, item, spider):
        return item


class WorldPopulationPipeline:
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collection = None
        self.primary_key = None
        self.client = None
        self.db = None

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def process_item(self, item, spider):
        if isinstance(item, CountryPopulationItem):
            self.mongo_collection = spider.settings.get('COUNTRY_POPULATION_COLLECTION')
            self.primary_key = spider.settings.get('COUNTRY_POPULATION_PK')
        elif isinstance(item, HistoricalPopulationItem):
            self.mongo_collection = spider.settings.get('HISTORICAL_POPULATION_COLLECTION')
            self.primary_key = spider.settings.get('HISTORICAL_POPULATION_PK')
        elif isinstance(item, ForecastPopulationItem):
            self.mongo_collection = spider.settings.get('FORECAST_POPULATION_COLLECTION')
            self.primary_key = spider.settings.get('FORECAST_POPULATION_PK')
        elif isinstance(item, CitiesPoulation):
            self.mongo_collection = spider.settings.get('CITY_POPULATION_COLLECTION')
            self.primary_key = spider.settings.get('CITY_POPULATION_PK')

        self.db[self.mongo_collection].update_one(
            {self.primary_key: item[self.primary_key]},
            {'$set': dict(item)},
            upsert=True
        )
        return item
