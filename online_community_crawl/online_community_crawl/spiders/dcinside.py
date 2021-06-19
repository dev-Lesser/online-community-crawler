import scrapy


class DcinsideSpider(scrapy.Spider):
    name = 'dcinside'
    allowed_domains = ['https://search.dcinside.com']
    start_urls = ['http://https://search.dcinside.com/']

    def parse(self, response):
        pass
