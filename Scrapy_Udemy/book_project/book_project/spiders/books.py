# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BooksSpider(CrawlSpider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths="//li[@class='next']/a"))
    )

    def parse_item(self, response):
        yield {
            'title' : response.xpath("normalize-space(//h1/text())").get(),
            'price' : response.xpath("//p[@class='price_color']/text()").get(),
            'genre' : response.xpath("//ul[@class='breadcrumb']/li[3]/a/text()").get()
        }
        
