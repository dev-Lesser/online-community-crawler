import scrapy


class PpomppuSpider(scrapy.Spider):
    name = 'ppomppu'
    allowed_domains = ['http://www.ppomppu.co.kr']
    start_urls = ['http://http://www.ppomppu.co.kr/']

    def parse(self, response):
        pass
