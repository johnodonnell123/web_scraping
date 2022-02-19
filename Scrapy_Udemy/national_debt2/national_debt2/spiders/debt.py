# -*- coding: utf-8 -*-
import scrapy


class DebtSpider(scrapy.Spider):
    name = 'debt'
    allowed_domains = ['www.worldpopulationreview.com']
    start_urls = ['https://www.worldpopulationreview.com/countries/countries-by-national-debt']

    def parse(self, response):
        rows = response.xpath("//table[@class='jsx-1878461898 table table-striped tp-table-body']/tbody/tr")
        for row in rows:
            yield {
                'name' : row.xpath(".//td[1]/a/text()").get(),
                'ratio' : row.xpath(".//td[2]/text()").get(),
                'pop' : row.xpath(".//td[3]/text()").get()
            }

            
