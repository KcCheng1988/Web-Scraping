import scrapy
from scrapy_splash import SplashRequest # must add to manage splash request


class CoinSpider(scrapy.Spider):
    name = 'coin'
    allowed_domains = ['web.archive.org']
    # start_urls = ['https://web.archive.org/web/20200116052415/https://www.livecoin.net/en']

    # add splash lua script here
    script = '''
        function main(splash, args)
            -- disable private mode 
            splash.private_mode_enabled = false
          
            url = args.url
            assert(splash:go(url))
            assert(splash:wait(1))
          
            rur_tab = assert(splash:select_all(".filterPanelItem___2z5Gb"))
            rur_tab[5]:mouse_click()
            assert(splash:wait(1))
            splash:set_viewport_full()
            return splash:html() 
        end
    '''

    def start_requests(self):
        # callback: what you want to do on the response of the start request
        # overwrite canonical scrapy start request method with splash request
        # endpoint: 'execute' because we want to execute the lua_script

        yield SplashRequest(url='https://web.archive.org/web/20200116052415/https://www.livecoin.net/en',
                            callback=self.parse,
                            endpoint='execute',
                            args={
                                'lua_source' : self.script
                            })


    def parse(self, response):
        print(response.body)
        for currency in response.xpath("//div[contains(@class, 'ReactVirtualized__Table__row tableRow___3EtiS')]"):
            yield {
                'currency' : currency.xpath(".//div[1]/div/text()").get(),
                'volume(24h)': currency.xpath(".//div[2]/span/text()").get()
            }

