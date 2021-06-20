import scrapy
from lxml import html
from online_community_crawl.items import OnlineCommunityCrawlItem


class MlbparkSpider(scrapy.Spider):
    name = 'mlbpark'
    def start_requests(self):
        # for page_num in range(100)
        urls = ['http://mlbpark.donga.com/mp/b.php?p={page_num}&m=search&b=bullpen&query=이준석&select=sct&user='.format(page_num=i) for i in range(1,100)] # 시간순 정렬 되어 있음
        for iurl in urls:
            yield scrapy.Request(
                url=iurl, 
                callback=self.parse_url
            )
    def parse_url(self, response):

        root = html.fromstring(response.text)
        titles = root.xpath('//table/tbody/tr/td/div[@class="tit"]/a/@alt')
        dates = root.xpath('//table/tbody/tr/td/span[@class="date"]/text()')
        urls = root.xpath('//table/tbody/tr/td/div[@class="tit"]/a/@href')
        results = list(zip(urls, titles, dates))
        for iurl, ititle, idate in results:
            yield scrapy.Request(
                url=iurl, 
                callback=self.parse,
                meta= {'title':ititle,'url': iurl,'date': idate}
            )
    def parse(self, response):
        post_items = OnlineCommunityCrawlItem()
        title = response.meta['title']
        date = response.meta['date']
        url = response.meta['url']

        root = html.fromstring(response.text)
        contents = ' '.join(root.xpath('//div[@class="ar_txt"]/text()'))

        vote_up = int(root.xpath('//span[@id="likeCnt"]/text()')[0])
        
        vote_down = 0

        post_items['title'] = title
        post_items['url'] = url
        post_items['date'] = date
        post_items['contents'] = contents
        post_items['vote_up'] = vote_up
        post_items['vote_down'] = vote_down
        post_items['source'] = 'mlbpark'
        yield post_items
