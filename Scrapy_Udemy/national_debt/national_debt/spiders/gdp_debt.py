# -*- coding: utf-8 -*-
import scrapy


class GdpDebtSpider(scrapy.Spider):
    name = 'gdp_debt'
    allowed_domains = ['www.worldpopulationreview.com/countries/countries-by-national-debt']
    start_urls = ['https://www.worldpopulationreview.com/countries/countries-by-national-debt/']

    def parse(self, response):
        rows = response.xpath("//tbody[@class='jsx-2642336383']/tr")
        for row in rows:
            country_name = row.xpath(".//td/a/text()").get()
            gdp_debt_ratio = row.xpath(".//td[2]/text()").get()
            population = row.xpath(".//td[3]/text()").get()

            yield {
                'country' : country_name,
                'gdp_debt_ratio' : gdp_debt_ratio,
                'population' : population
            }
