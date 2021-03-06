# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.shell import inspect_response

from ..items import ImdbItem


class MoviesSpider(CrawlSpider):
    name = 'movies'
    allowed_domains = ['imdb.com']
    start_urls = ["http://www.imdb.com/search/title/?title_type=feature&languages=en&sort=num_votes,desc&view=simple"]
    
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//span[@class='lister-item-header']/span/a"), callback='parse_1', follow=True),
        Rule(LinkExtractor(restrict_xpaths="(//a[@class='lister-page-next next-page'])[2]"))
    )


    def parse_1(self, response):
        # inspect_response(response,self)
        item = ImdbItem()
        
        item['movie_url'] = response.url
        item['title'] = response.xpath("//h1[@data-testid='hero-title-block__title']/text()").get()
        item['rating'] = response.xpath("(//span[@class='AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV'])[1]/text()").get()
        item['date'] = response.xpath("(//li[@class='ipc-inline-list__item'])[1]/span/text()").get()
        item['genres'] = response.xpath("//li[@data-testid='storyline-genres']//a/text()").getall()
        item['total_ratings'] = response.xpath("(//div[@class='AggregateRatingButton__TotalRatingAmount-sc-1ll29m0-3 jkCVKJ'])[2]/text()").get()
        item['num_user_reviews'] = response.xpath("(//span[@class='score'])[1]/text()").get()
        item['top_cast'] = response.xpath("//a[@data-testid='title-cast-item__actor']/text()").getall()
        item['director'] = response.xpath("(//section[@data-testid='title-cast']/ul/li)[1]//a/text()").get()
        item['writers'] = response.xpath("//section[@data-testid='title-cast']/ul/li[@class='ipc-metadata-list__item'][2]/div//a/text()").getall()
        item['storyline'] = response.xpath("//div[@class='Storyline__StorylineWrapper-sc-1b58ttw-0 iywpty']/div[1]/div/div/text()").get()
        item['plot_tags'] = response.xpath("//div[@class='Storyline__StorylineWrapper-sc-1b58ttw-0 iywpty']/div[2]/a/span/text()").getall()
        item['language'] = response.xpath("//li[@data-testid='title-details-languages']/div//a/text()").getall()
        
        summary_url = response.xpath("//ul[@data-testid='storyline-plot-links']/li/a/@href").get()
    
        if summary_url:
            yield response.follow(url=summary_url, callback=self.parse_2, meta={'item': item})
        else:
            yield item
        
    def parse_2(self, response):
        item=response.meta['item']
        item['summaries'] = response.xpath("//ul[@id='plot-summaries-content']/li//p/text()").getall(),
        item['synopsis'] = response.xpath("//ul[@id='plot-synopsis-content']//text()").getall()
        
        yield item


    