import scrapy
from lxml import html
from online_community_crawl.items import OnlineCommunityCrawlItem
class IlbeSpider(scrapy.Spider):
    name = 'ilbe'

    def start_requests(self):
        # for page_num in range(100)
        urls = ['https://www.ilbe.com/search?docType=doc&searchType=title_content&page={page_num}&q=이준석'.format(page_num=i) for i in range(1,200)] # 시간순 정렬 되어 있음
        for iurl in urls:
            yield scrapy.Request(
                url=iurl, 
                callback=self.parse_url
            )
    def parse_url(self, response):

        root = html.fromstring(response.text)
        tree = root.xpath('//div[@class="search-list"]/ul/li')
        titles = [''.join(i.xpath('.//a[@class="title"]/text()|.//a[@class="title"]/strong/text()')) for i in tree]
        dates = [i.xpath('.//span[@class="date"]/text()')[0].split()[0] for i in tree]
        urls = [i.xpath('.//a/@href')[0] for i in tree]
        results = list(zip(urls, titles, dates))
        for iurl, ititle, idate in results:
            yield scrapy.Request(
                url='https://www.ilbe.com'+ iurl, 
                callback=self.parse,
                meta= {'title':ititle,'url':'https://www.ilbe.com'+ iurl,'date': idate}
            )
    def parse(self, response):
        post_items = OnlineCommunityCrawlItem()
        title = response.meta['title']
        date = response.meta['date']
        url = response.meta['url']

        root = html.fromstring(response.text)
        contents = ' '.join([i.replace(u'\xa0',u' ').strip() for i in root.xpath('//div[@class="post-content"]/p/text()|//div[@class="post-content"]/text()')])
        votes_up_len = len(root.xpath('//button[@id="btn_vote_up"]/span/em/text()'))
        votes_down_len = len(root.xpath('//button[@id="btn_vote_down"]/span/em/text()'))
        vote_up = int(root.xpath('//button[@id="btn_vote_up"]/span/em/text()')[0]) if votes_up_len>0 else 0
        vote_down = int(root.xpath('//button[@id="btn_vote_down"]/span/em/text()')[0]) if votes_down_len>0 else 0

        post_items['title'] = title
        post_items['url'] = url
        post_items['date'] = date
        post_items['contents'] = contents
        post_items['vote_up'] = vote_up
        post_items['vote_down'] = vote_down
        post_items['source'] = 'ilbe'
        yield post_items


