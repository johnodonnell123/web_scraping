# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import ImdbItem

df = pd.read_csv(r'starts_df.csv')
starts = df['links'].astype(str).tolist()


class SinglePageSpider(CrawlSpider):
    name = 'single_page'
    allowed_domains = ['imdb.com']
    start_urls = starts
    
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3[@class='lister-item-header']/a"), callback='parse_1', follow=True),
    )


    def parse_1(self, response):
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
