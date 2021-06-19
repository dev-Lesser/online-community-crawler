import scrapy


class FmkoreaSpider(scrapy.Spider):
    name = 'fmkorea'
    allowed_domains = ['https://www.fmkorea.com']
    start_urls = ['http://https://www.fmkorea.com/']

    def parse(self, response):
        pass
