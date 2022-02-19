# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

# Check Pipelines.py and Settings.py

class CrawlerSpiderTemplateSpider(CrawlSpider):
    name = 'crawler_spider_template'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/search/title/?groups=top_250&sort=user_rating']

    # Rules tuple must contain >= 1 Rule object, tells the spider which links to follow
    # Order of Rules does matter: First rule should pass response to parse method, second rule should handle pagination
    # 3 args: LinkExtractor, callback, follow
    rules = (
        Rule(
            LinkExtractor(restrict_xpaths="//h3[@class='lister-item-header']/a"), # What links to extract
            callback = 'parse_item',  # Where to send the response object, must be a string
            follow = True), # Send request or not? 
        Rule(
            LinkExtractor(restrict_xpaths="(//a[@class='lister-page-next next-page'])[2]")) # Pagination link
            # No other arguments needed, we only want to follow the link, the previous Rule will handle the scraping
    )

    # Define parse method to handle the data from each page, response input provided from the first Rule object in rules tuple
    def parse_item(self, response):
        yield {
            'title' : response.xpath("//div[@class='title_wrapper']/h1/text()").get(),
            'year' : response.xpath("//span[@id='titleYear']/a/text()").get(),
            'duration' : response.xpath("normalize-space(//div[@class='subtext']/time/text())").get(), # normalize-space Xpath function used to strip whitespace
            'genre' : response.xpath("//div[@class='subtext']/a/text()").get(),
            'rating' : response.xpath("//span[@itemprop='ratingValue']/text()").get(),
            'movie_url' : response.url
            
        }
