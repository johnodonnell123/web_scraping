# -*- coding: utf-8 -*-
import scrapy
from scrapy.shell import inspect_response 

class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country']

    def parse(self, response):
        # countries = response.xpath("//td/a")
        # for country in countries:
        #     name = country.xpath(".//text()").get()
        #     link = country.xpath(".//@href").get()

        yield response.follow(url="https://www.worldometers.info/world-population/china-population/",callback=self.parse_country, meta = {'name': name})
    
    def parse_country(self, response):
        rows = response.xpath("//div[@class='table-responsive'][1]/table/tbody/tr")
        name = response.request.meta['name']
        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            pop = row.xpath(".//td[2]/strong/text()").get()

            yield {
                'name': name,
                'year' : year,
                'pop' : pop
            }

