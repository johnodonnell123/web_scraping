# -*- coding: utf-8 -*-
import scrapy
from scrapy.shell import inspect_response
from scrapy_splash import SplashRequest


class LogsSpider(scrapy.Spider):
    name = 'logs'

    api = 33053026690000

    api_quotes = f"'{api}'"

    script = '''
        function main(splash, args)
            headers = {['Authorization'] = 'Basic am9obm9kb25uZWxsOiNIdW1ibGU0VFg='}
            splash:set_custom_headers(headers)
            assert(splash:go(args.url))
            input_box = assert(splash:select("input[name=APINumber]"))
            input_box:focus()
            input_box:send_text(''' + api_quotes + ''')
            assert(splash:wait(0.5))
            btn = assert(splash:select("input[value='Get Scout Ticket Data']"))
            btn:mouse_click()
            assert(splash:wait(3))
            return {html = splash:html()}
        end      
'''
    def start_requests(self):
        yield SplashRequest(url="https://www.dmr.nd.gov/oilgas/feeservices/getscoutticket.asp",callback = self.parse, endpoint = "execute", args = {
            'lua_source': self.script
        })
    
    def parse(self, response): 
        #inspect_response(response, self)
        yield {
            'las_url' : response.xpath("//a[contains(@href,'.las')]/@href").get()
        }
