import scrapy


class MlbparkSpider(scrapy.Spider):
    name = 'mlbpark'
    allowed_domains = ['http://mlbpark.donga.com/']
    start_urls = ['http://http://mlbpark.donga.com//']

    def parse(self, response):
        pass
