# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.shell import inspect_response


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/api/quotes?page=1']

    def parse(self, response):
        # inspect_response(response,self)
        resp = json.loads(response.body)
        quotes = resp.get('quotes')
        for quote in quotes:
            yield {
                'author' : quote.get('author').get('name'),
                'tags' : quote.get('tags'),
                'quote_text' : quote.get('text')
            }
        
        has_next = resp.get('has_next')
        if has_next:
            next_page_number = resp.get('page') + 1
            yield scrapy.Request(
                url = f'http://quotes.toscrape.com/api/quotes?page={next_page_number}',
                callback=self.parse
            )
