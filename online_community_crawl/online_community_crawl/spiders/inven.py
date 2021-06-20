import scrapy
from lxml import html
from online_community_crawl.items import OnlineCommunityCrawlItem

class InvenSpider(scrapy.Spider):
    name = 'inven'

    def start_requests(self):
        # for page_num in range(100)
        urls = ['https://www.inven.co.kr/search/webzine/article/이준석/{page_num}'.format(page_num=i) for i in range(1,2)] # 시간순 정렬 되어 있음
        for iurl in urls:
            yield scrapy.Request(
                url=iurl, 
                callback=self.parse_url
            )
    def parse_url(self, response):

        root = html.fromstring(response.text)
        titles = [''.join(i.xpath('./a/text()|./a/b/text()')) for i in root.xpath('//ul[@class="news_list"]/li[@class="item"]/h1')]
        dates = [''.join(i.xpath('./p[@class="date"]/text()')) for i in root.xpath('//ul[@class="news_list"]/li[@class="item"]/div[@class="item_info clearfix"]')]
        urls = [''.join(i.xpath('./a/@href')) for i in root.xpath('//ul[@class="news_list"]/li[@class="item"]/h1')]
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
        contents = ' '.join([i.strip() for i in root.xpath('//div[@id="powerbbsContent"]/*/text()|//div[@id="powerbbsContent"]/*/*/text()') if i.strip()!=''])

        vote_up_length = len(root.xpath('//span[@class="reqnum reqblue"]'))
        vote_up = int(root.xpath('//span[@class="reqnum reqblue"]/span/text()')[0]) if vote_up_length else 0 
        
        vote_down_length = len(root.xpath('//span[@class="reqnum reqred"]'))
        vote_down = int(root.xpath('//span[@class="reqnum reqred"]/span/text()')[0]) if vote_down_length else 0 #게시판에 따라 있는 게 있고 없는게 있음

        post_items['title'] = title
        post_items['url'] = url
        post_items['date'] = date
        post_items['contents'] = contents
        post_items['vote_up'] = vote_up
        post_items['vote_down'] = vote_down
        post_items['source'] = 'inven'
        yield post_items
