# -*- coding: utf-8 -*-
import scrapy


class DebtspiderSpider(scrapy.Spider):
    name = 'debtspider'
    allowed_domains = ['https://www.worldpopulationreview.com/countries/countries-by-national-debt/']
    start_urls = ['https://www.worldpopulationreview.com/countries/countries-by-national-debt/']

    def parse(self, response):
        rows = response.xpath("//tbody[@class='jsx-2642336383']/tr")
        for row in rows:
            name = row.xpath(".//td/a/text()").get()
            ratio = row.xpath(".//td[2]/text()").get()
            pop = row.xpath(".//td[3]/text()").get()

            yield {
                'name' : name,
                'ratio' : ratio,
                'pop' : pop
            }