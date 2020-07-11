# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class CountryPopulationItem(scrapy.Item):
    country = scrapy.Field()
    population = scrapy.Field()
    yearly_change = scrapy.Field()
    net_change = scrapy.Field()
    density = scrapy.Field()
    land_area = scrapy.Field()
    migrants = scrapy.Field()
    fert_rate = scrapy.Field()
    med_age = scrapy.Field()
    urban_pop = scrapy.Field()
    world_share = scrapy.Field()
