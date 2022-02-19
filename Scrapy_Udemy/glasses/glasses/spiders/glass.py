# -*- coding: utf-8 -*-
import scrapy

class GlassSpider(scrapy.Spider):
    name = 'glass'
    allowed_domains = ['www.glassesshop.com']

    def start_requests(self):
        yield scrapy.Request(url="https://www.glassesshop.com/bestsellers", callback=self.parse, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'})

    def parse(self, response):
        products = response.xpath("//div[@id='product-lists']/div")
        for product in products:
            yield {
                'prod_url': product.xpath(".//div[@class='p-title']/a/@href").get(),
                'prod_img_link': product.xpath(".//img[@class='lazy d-block w-100 product-img-default']/@data-src").get(),
                'prod_name': product.xpath(".//div[@class='p-title']/a/@title").get(),
                'prod_price': product.xpath(".//div[@class='p-price']/div/span/text()").get(),
            }
        next_page = response.xpath("//a[@rel='next']/@href").get()

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'})
