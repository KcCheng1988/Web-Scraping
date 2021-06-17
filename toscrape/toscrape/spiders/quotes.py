import scrapy
from scrapy_splash import SplashRequest
import logging

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    # start_urls = ['http://quotes.toscrape.com/js']

    script = '''
        function main(splash, args)
          headers = {
            ['User-Agent'] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
          }
          splash:set_custom_headers(headers)
          
          url = args.url
          assert(splash:go(url))
          assert(splash:wait(1))
                   
          splash:set_viewport_full()
          return splash:html()
        end
    '''

    def start_requests(self):
        yield SplashRequest(url="http://quotes.toscrape.com/js",
                            callback=self.parse,
                            endpoint='execute',
                            args={
                                'lua_source' : self.script
                            })

    def parse(self, response):
        for quote in response.xpath("//div[@class='quote']"):
            text = quote.xpath(".//span[@class='text']/text()").get()
            author = quote.xpath(".//span/small[@class='author']/text()").get()
            tags = quote.xpath(".//div[@class='tags']/a/text()").extract()

            yield {
                'quote' : text,
                'author' : author,
                'tags' : tags
            }

        rel_url = response.xpath("//li[@class='next']/a[contains(@href, '/js/page')]/@href").get()
        next_url = f"http://quotes.toscrape.com{rel_url}"
        if next_url:
            yield SplashRequest(url=next_url,
                                callback=self.parse,
                                endpoint='execute',
                                args={
                                    'lua_source' : self.script
                                })
