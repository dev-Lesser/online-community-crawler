import scrapy


class ClienSpider(scrapy.Spider):
    name = 'clien'
    allowed_domains = ['https://www.clien.net']
    start_urls = ['http://https://www.clien.net/']

    def parse(self, response):
        pass
