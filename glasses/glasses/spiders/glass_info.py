import scrapy

class GlassInfoSpider(scrapy.Spider):
    name = 'glass_info'
    allowed_domains = ['www.glassesshop.com']
    start_urls = ['https://www.glassesshop.com/bestsellers']

    # def start_requests(self):
    #     yield scrapy.Request(url="https://www.glassesshop.com/bestsellers",
    #                          callback=self.parse,
    #                          headers={
    #                              'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
    #                          })

    def parse(self, response):
        products = response.xpath("//div[@id='product-lists']/div")
        for product in products:
            product_name = product.xpath(".//descendant::div[@class='p-title']/a[1]/text()").get()
            product_price = product.xpath(".//descendant::div[@class='p-price']/div[1]/span/text()").get()
            product_url = product.xpath(".//descendant::div[@class='p-title']/a/@href").get()
            product_img_link = product.xpath(".//descendant::div[@class='product-img-outer']/a[1]/img[1]/@data-src").get()

            yield {
                'product_name' : product_name,
                'product_price' : product_price,
                'product_url' : product_url,
                'product_img_link' : product_img_link,
            }

        nextPage = response.xpath("//ul[@class='pagination'][1]/li[position()=last()]/a/@href").get()
        if nextPage:
            yield scrapy.Request(url=nextPage,
                                 callback=self.parse,
                                 headers={
                                     'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
                                 })
