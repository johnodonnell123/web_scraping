# -*- coding: utf-8 -*-

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/search/title/?groups=top_250&sort=user_rating']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3[@class='lister-item-header']/a"), callback='parse_item', follow=True),
        #Rule(LinkExtractor(restrict_xpaths="(//a[@class='lister-page-next next-page'])[2]"))
    )

    def parse_item(self, response):
        yield {
            'title' : response.xpath("//div[@class='TitleBlock__TitleContainer-sc-1nlhx7j-1 jxsVNt']/h1/text()").get(),
#             'year' : response.xpath("//span[@id='titleYear']/a/text()").get(),
#             'duration' : response.xpath("normalize-space(//div[@class='subtext']/time/text())").get(),
#             'genre' : response.xpath("//div[@class='subtext']/a/text()").get(),
#             'rating' : response.xpath("//span[@itemprop='ratingValue']/text()").get(),
#             'movie_url' : response.url
            
        }
