import scrapy
import logging

class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']


    def parse(self, response):
        # title = response.xpath("//h1/text()").get()
        countries = response.xpath("//tr/td/a")
        for country in countries:
            name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()

            # construct full url link
            # absolute_url = f"https://www.worldometers.info{link}" # option 1
            absolute_url = response.urljoin(link) #option 2

            # send GET request with the full url
            yield scrapy.Request(url=absolute_url,
                                 callback=self.parse_country,
                                 meta={'country_name' : name})

            # option 3: without the need to construct absolute url
            # yield response.follow(url=link,
            #                       callback=self.parse_country)

    def parse_country(self, response):
        name = response.request.meta['country_name']
        pop_rows = response.xpath(
            "//h2[contains(text(),'historical')]/following::table[1]/tbody/tr"
        )

        for row in pop_rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()
            yield {
                'name': name,
                'year' : year,
                'population' : population
            }

