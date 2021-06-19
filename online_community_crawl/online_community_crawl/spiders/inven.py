import scrapy


class InvenSpider(scrapy.Spider):
    name = 'inven'
    allowed_domains = ['https://www.inven.co.kr']
    start_urls = ['http://https://www.inven.co.kr/']

    def parse(self, response):
        pass
