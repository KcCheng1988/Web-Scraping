import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

class CoinSpiderSelenium(scrapy.Spider):
    name = 'coin_selenium'
    allowed_domains = ['web.archive.org']
    start_urls = ['https://web.archive.org/web/20200116052415/https://www.livecoin.net/en']

    def __init__(self):
        # do everything related to selenium
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        chrome_path = './chromedriver'
        driver = webdriver.Chrome(executable_path=chrome_path,
                                  options=chrome_options)
        driver.set_window_size(1920,1080) # the number of items shown on the browser depends on the window resolution
        driver.get('https://web.archive.org/web/20200116052415/https://www.livecoin.net/en')

        rur_tab = driver.find_elements_by_class_name("filterPanelItem___2z5Gb ")
        rur_tab[4].click() # get and click on the RUR tab

        self.html = driver.page_source
        # the html is a string. You need to convert the string to selector object in order
        # to select element by xpath
        driver.close()

    def parse(self, response):
        resp = Selector(text=self.html)
        for currency in resp.xpath("//div[contains(@class, 'ReactVirtualized__Table__row tableRow___3EtiS')]"):
            yield {
                'currency': currency.xpath(".//div[1]/div/text()").get(),
                'volume(24h)': currency.xpath(".//div[2]/span/text()").get()
            }

