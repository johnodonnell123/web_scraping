# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest


class QuotesLoginSpider(scrapy.Spider):
    name = 'quotes_login'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['https://quotes.toscrape.com/login']

    def parse(self, response):
        yield FormRequest.from_response ( 
            response,
            formxpath = '//form',
            formdata = { 
                'csrf_token' : response.xpath("//input[@name='csrf_token']/@value").get(),
                'username' : 'admin',
                'password' : 'admin'
            },
            callback = self.after_login
        )
    
    def after_login(self, response):
        if response.xpath("//a[@href='/logout']/text()").get():
            print('We logged in!')
