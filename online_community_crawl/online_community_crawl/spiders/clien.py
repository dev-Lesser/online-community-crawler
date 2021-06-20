import scrapy
from lxml import html
from online_community_crawl.items import OnlineCommunityCrawlItem


class ClienSpider(scrapy.Spider):
    name = 'clien'
    def start_requests(self):
        # for page_num in range(100)
        urls = ['https://www.clien.net/service/search?q=이준석&sort=recency&p={page_num}&boardCd=&isBoard=false'.format(page_num=i) for i in range(0,100)] # 시간순 정렬 되어 있음
        for iurl in urls:
            yield scrapy.Request(
                url=iurl, 
                callback=self.parse_url
            )
    def parse_url(self, response):

        root = html.fromstring(response.text)
        titles =root.xpath('//div[@class="contents_jirum"]/div[contains(@class,"list_item")]/div/span/a/@title')
        dates = [i.split()[0] for i in root.xpath('//div[@class="contents_jirum"]/div[contains(@class,"list_item")]/div[@class="list_time"]/span/span[@class="timestamp"]/text()')]
        urls = root.xpath('//div[@class="contents_jirum"]/div[contains(@class,"list_item")]/div/span/a/@href')
        results = list(zip(urls, titles, dates))
        for iurl, ititle, idate in results:
            yield scrapy.Request(
                url='https://www.clien.net/'+iurl, 
                callback=self.parse,
                meta= {'title':ititle,'url': 'https://www.clien.net/'+iurl, 'date': idate}
            )
    def parse(self, response):
        post_items = OnlineCommunityCrawlItem()
        title = response.meta['title']
        date = response.meta['date']
        url = response.meta['url']

        root = html.fromstring(response.text)
        contents = ' '.join([i.strip() for i in root.xpath('//div[@class="post_article"]/text()|//div[@class="post_article"]/*/text()') if i.strip()!=''])

        vote_up = int(root.xpath('//a[contains(@class,"symph_count")]/*/text()')[0])
        
        vote_down = 0

        post_items['title'] = title
        post_items['url'] = url
        post_items['date'] = date
        post_items['contents'] = contents
        post_items['vote_up'] = vote_up
        post_items['vote_down'] = vote_down
        post_items['source'] = 'clien'
        yield post_items
