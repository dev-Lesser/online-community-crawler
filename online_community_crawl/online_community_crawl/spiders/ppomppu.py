import scrapy
from lxml import html
from online_community_crawl.items import OnlineCommunityCrawlItem

class PpomppuSpider(scrapy.Spider):
    name = 'ppomppu'

    def start_requests(self):
        # for page_num in range(100)
        urls = ['http://www.ppomppu.co.kr/search_bbs.php?search_type=sub_memo&page_no={page_num}&keyword=이준석&page_size=20&bbs_id=&order_type=date&bbs_cate=2'.format(page_num=i) for i in range(1,100)] # 시간순 정렬 되어 있음
        for iurl in urls:
            yield scrapy.Request(
                url=iurl, 
                callback=self.parse_url
            )
    def parse_url(self, response):

        root = html.fromstring(response.text)
        tree = root.xpath('//div[@class="results_board"]/div[@class="conts"]')
        titles = [''.join(i.xpath('.//div[@class="content"]/span[@class="title"]/a/text()|.//div[@class="content"]/span[@class="title"]/a/b/text()')) for i in tree]
        dates =[i.xpath('.//p[@class="desc"]/span[3]/text()')[0].replace('.','-') for i in tree]
        urls = [i.xpath('.//div[@class="content"]/span[@class="title"]/a/@href')[0] for i in tree]
        results = list(zip(urls, titles, dates))
        for iurl, ititle, idate in results:
            yield scrapy.Request(
                url='http://www.ppomppu.co.kr/'+iurl, 
                callback=self.parse,
                meta= {'title':ititle,'url': iurl,'date': idate}
            )
    def parse(self, response):
        post_items = OnlineCommunityCrawlItem()
        title = response.meta['title']
        date = response.meta['date']
        url = response.meta['url']

        root = html.fromstring(response.text)
        contents = ' '.join([i.strip() for i in root.xpath('//td[@class="board-contents"]/*/text()') if i.strip() != ''])

        vote_up = int([i.strip() for i in root.xpath('//p[@class="btn_recommand"]/text()') if i.strip()!=''][0])
        
        vote_down = int([i.strip() for i in root.xpath('//p[@class="btn_different"]/text()') if i.strip()!=''][0])

        post_items['title'] = title
        post_items['url'] = url
        post_items['date'] = date
        post_items['contents'] = contents
        post_items['vote_up'] = vote_up
        post_items['vote_down'] = vote_down
        post_items['source'] = 'ppomppu'
        yield post_items
