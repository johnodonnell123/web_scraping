# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.shell import inspect_response

# def clean(item):
#     if ite


class MoviesSpider(CrawlSpider):
    name = 'movies'
    allowed_domains = ['imdb.com']
    start_urls = ["https://www.imdb.com/search/title/?title_type=feature&languages=en&sort=boxoffice_gross_us,desc"]
    
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3[@class='lister-item-header']/a"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths="(//a[@class='lister-page-next next-page'])[2]"))
    )


    def parse_item(self, response):
        # inspect_response(response,self)
        yield {
            'title' : response.xpath("(//h1/text())[1]").get(),
            'date' : response.xpath("//a[@title='See more release dates']/text()").get().rstrip(),
            'star_rating' : response.xpath("//span[@itemprop='ratingValue']/text()").get(),
            'num_ratings' : response.xpath("//span[@itemprop='ratingCount']/text()").get().replace(",",''),
            'genres' : [i.strip() for i in response.xpath('//div[@class="see-more inline canwrap"]//a[contains(@href , "genres=")]/text()').getall()],
            'run_time' : response.xpath("(//time/text())[1]").get().strip(),
            'director' : response.xpath("(//div[@class='credit_summary_item'])[1]/a/text()").get(),
            'writer' : response.xpath("(//div[@class='credit_summary_item'])[2]/a/text()").get(),
            'stars' : response.xpath("(//div[@class='credit_summary_item'])[3]/a/text()").getall()[:-1],
            'plot_keywords' : response.xpath("//span[@class='itemprop']/text()").getall(),
            'budget' : response.xpath("(//h4[contains(text(), 'Budget')]/following-sibling::node())[1]").get(),
            'cum_worldwide_gross' : response.xpath("(//h4[contains(text(), 'Cumulative Worldwide Gross:')]/following-sibling::node())[1]").get(),
            'production_company' : response.xpath("(//h4[contains(text(), 'Production Co')]/following-sibling::a/text())[1]").get()
        }

