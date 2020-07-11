import scrapy
from scraper.items import CountryPopulationItem


class CountryPopulationSpider(scrapy.Spider):

    name = 'country_pop_spider'

    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    custom_settings = {
        'MONGO_COLLECTION': 'country_population',
        'PRIMARY_KEY': 'country'
    }

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
