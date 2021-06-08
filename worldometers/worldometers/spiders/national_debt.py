import scrapy


class NationalDebtSpider(scrapy.Spider):
    name = 'national_debt'
    allowed_domains = ['worldpopulationreview.com']
    start_urls = ['https://worldpopulationreview.com/countries/countries-by-national-debt']

    def parse(self, response):
        countries = response.xpath("//h2[contains(text(), 'National Debt')]/preceding::tbody/tr")
        for country in countries:
            name = country.xpath(".//td/a/text()").get()
            debt = country.xpath(".//td[2]/text()").get()

            yield({
                'country' : name,
                'national_debt' : debt
            })


