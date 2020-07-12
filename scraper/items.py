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


class HistoricalPopulationItem(scrapy.Item):
    country = scrapy.Field()
    historical_pop = scrapy.Field()


class ForecastPopulationItem(scrapy.Item):
    country = scrapy.Field()
    forecast_pop = scrapy.Field()


class DetailPopulationItem(scrapy.Item):
    year = scrapy.Field()
    population = scrapy.Field()
    yearly_percent_change = scrapy.Field()
    yearly_change = scrapy.Field()
    migrants = scrapy.Field()
    med_age = scrapy.Field()
    fer_rate = scrapy.Field()
    density = scrapy.Field()
    urban_pop_percentage = scrapy.Field()
    urban_pop = scrapy.Field()
    country_share_population = scrapy.Field()
    world_population = scrapy.Field()
    global_rank = scrapy.Field()


class CitiesPoulation(scrapy.Item):
    country = scrapy.Field()
    cities_pop = scrapy.Field()
