# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.shell import inspect_response

from ..items import UserItem

class UsersSpider(CrawlSpider):
    name = 'users'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/search/title/?title_type=feature&languages=en&sort=num_votes,desc&view=simple']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//span[@class='lister-item-header']/span/a"), callback='parse_1', follow=True),
        Rule(LinkExtractor(restrict_xpaths="(//a[@class='lister-page-next next-page'])[2]"))
    )

    def parse_1(self, response):
        reviews_url = response.xpath("(//ul[@data-testid='reviewContent-all-reviews']/li/a/@href)[1]").get()
        if reviews_url:
            yield response.follow(url=reviews_url, callback=self.parse_2)

    def parse_2(self, response):
        item = UserItem()
        movie = response.xpath("//h3[@itemprop='name']/a/text()").get()
        reviews = response.xpath("//div[@class='review-container']")
        for review in reviews:
            item['rating'] = review.xpath(".//div[@class='lister-item-content']/div/span/span[1]/text()").get()
            item['rating_date'] = review.xpath(".//span[@class='review-date']/text()").get()
            item['user_name'] = review.xpath(".//div[@class='display-name-date']/span/a/text()").get()
            item['movie'] = movie
            
            yield item