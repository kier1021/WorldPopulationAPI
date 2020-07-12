import scrapy
from scraper.items import CountryPopulationItem, DetailPopulationItem, HistoricalPopulationItem, \
    ForecastPopulationItem, \
    CitiesPoulation

import re


class CountryPopulationSpider(scrapy.Spider):

    name = 'country_pop_spider'

    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    base_url = 'https://www.worldometers.info'

    def __init___(self):
        pass

    def parse(self, response):
        for row in response.xpath('//table/tbody/tr'):
            cp_item = CountryPopulationItem()
            cp_item['country'] = row.xpath('td[2]//text()').get()
            cp_item['population'] = row.xpath('td[3]//text()').get()
            cp_item['yearly_change'] = row.xpath('td[4]//text()').get()
            cp_item['net_change'] = row.xpath('td[5]//text()').get()
            cp_item['density'] = row.xpath('td[6]//text()').get()
            cp_item['land_area'] = row.xpath('td[7]//text()').get()
            cp_item['migrants'] = row.xpath('td[8]//text()').get()
            cp_item['fert_rate'] = row.xpath('td[9]//text()').get()
            cp_item['med_age'] = row.xpath('td[10]//text()').get()
            cp_item['urban_pop'] = row.xpath('td[11]//text()').get()
            cp_item['world_share'] = row.xpath('td[12]//text()').get()
            yield cp_item
            #
            url = row.xpath('td[2]/a/@href').get()
            yield scrapy.Request(url=self.base_url + url, callback=self.parse_country)

    def parse_country(self, response):
        reg = re.search('/world-population/([\w-]+)-population/', response.url)
        country = ' '.join(reg.group(1).split('-')) if reg is not None else 'not available'
        tables = response.xpath('//table[contains(@class, "table")]')
        historical_pop_table = tables[0]
        forecast_table = tables[1]

        hist_item = HistoricalPopulationItem()
        hist_item['country'] = country
        hist_item['historical_pop'] = []

        fore_item = ForecastPopulationItem()
        fore_item['country'] = country
        fore_item['forecast_pop'] = []

        city_item = CitiesPoulation()
        city_item['country'] = country
        city_item['cities_pop'] = []

        # loop through historical table
        for historical_row in historical_pop_table.xpath('tbody/tr'):
            dp_item = DetailPopulationItem()
            if len(tables) < 3:
                dp_item = self.__get_inc_item(dp_item, historical_row)
            else:
                dp_item = self.__get_complete_item(dp_item, historical_row)
            hist_item['historical_pop'].append(dict(dp_item))
        yield hist_item

        # loop through forecast table
        for forecast_row in forecast_table.xpath('tbody/tr'):
            dp_item = DetailPopulationItem()
            if len(tables) < 3:
                dp_item = self.__get_inc_item(dp_item, forecast_row)
            else:
                dp_item = self.__get_complete_item(dp_item, forecast_row)
            fore_item['forecast_pop'].append(dict(dp_item))
        yield fore_item

        # check if there is a city table
        if len(tables) == 3:
            # loop through city table
            for cities_row in tables[2].xpath('tbody/tr'):
                city_item['cities_pop'].append({
                    'city': cities_row.xpath('td[2]//text()').get(),
                    'population': cities_row.xpath('td[3]//text()').get(),
                })
            yield city_item

    def __get_inc_item(self, item, pointer):
        item['year'] = pointer.xpath('td[1]//text()').get()
        item['population'] = pointer.xpath('td[2]//text()').get()
        item['yearly_percent_change'] = pointer.xpath('td[3]//text()').get()
        item['yearly_change'] = pointer.xpath('td[4]//text()').get()
        item['migrants'] = None
        item['med_age'] = None
        item['fer_rate'] = None
        item['density'] = pointer.xpath('td[5]//text()').get()
        item['urban_pop_percentage'] = pointer.xpath('td[6]//text()').get()
        item['urban_pop'] = pointer.xpath('td[7]//text()').get()
        item['country_share_population'] = pointer.xpath('td[8]//text()').get()
        item['world_population'] = pointer.xpath('td[9]//text()').get()
        item['global_rank'] = pointer.xpath('td[10]//text()').get()
        return item

    def __get_complete_item(self, item, pointer):
        item['year'] = pointer.xpath('td[1]//text()').get()
        item['population'] = pointer.xpath('td[2]//text()').get()
        item['yearly_percent_change'] = pointer.xpath('td[3]//text()').get()
        item['yearly_change'] = pointer.xpath('td[4]//text()').get()
        item['migrants'] = pointer.xpath('td[5]//text()').get()
        item['med_age'] = pointer.xpath('td[6]//text()').get()
        item['fer_rate'] = pointer.xpath('td[7]//text()').get()
        item['density'] = pointer.xpath('td[8]//text()').get()
        item['urban_pop_percentage'] = pointer.xpath('td[9]//text()').get()
        item['urban_pop'] = pointer.xpath('td[10]//text()').get()
        item['country_share_population'] = pointer.xpath('td[11]//text()').get()
        item['world_population'] = pointer.xpath('td[12]//text()').get()
        item['global_rank'] = pointer.xpath('td[13]//text()').get()
        return item

