import scrapy
import time

class SpecsSpider(scrapy.Spider):
    name = 'specs'
    allowed_domains = ['www.ultimatespecs.com']
    start_urls = ['https://www.ultimatespecs.com/car-specs']

    def parse(self, response):
        for model in response.xpath("//div[@class='table_makes']/div[@class='row']/div[contains(@class, 'makelinks')]"):
            car_url = model.xpath(".//a/@href").get()
            car_url = response.urljoin(car_url)
            yield scrapy.Request(url=car_url,
                                 callback=self.to_full_list)

    def to_full_list(self, response):
        full_list_url = response.xpath("//a[contains(text(), 'View Full')]/@href").get()
        full_list_url = response.urljoin(full_list_url)
        yield scrapy.Request(url=full_list_url,
                             callback=self.to_car_model)


    def to_car_model(self, response):
        for model in response.xpath("//div[@class='someOtherRow']/a[contains(text(), 'Specs')]"):
            specs_url = model.xpath(".//@href").get()
            specs_url = response.urljoin(specs_url)
            yield scrapy.Request(url=specs_url,
                                 callback=self.get_specs)

    def get_specs(self, response):
        length_text = response.xpath("//td[contains(text(), 'Length')]/following::td[1]/text()").get()
        width_text = response.xpath("//td[contains(text(), 'Width')]/following::td[1]/text()").get()
        height_text = response.xpath("//td[contains(text(), 'Height')]/following::td[1]/text()").get()
        yield{
            'length' : length_text,
            'width' : width_text,
            'height' : height_text
        }

