import scrapy
from lxml import html
from online_community_crawl.items import OnlineCommunityCrawlItem
class DcinsideSpider(scrapy.Spider):
    name = 'dcinside'

    def start_requests(self):
        # for page_num in range(100)
        urls = ['https://search.dcinside.com/post/p/{page_num}/sort/latest/q/.EC.9D.B4.EC.A4.80.EC.84.9D'.format(page_num=i) for i in range(1,120)] # 시간순 정렬 되어 있음
        for iurl in urls:
            yield scrapy.Request(
                url=iurl, 
                callback=self.parse_url
            )
    def parse_url(self, response):

        root = html.fromstring(response.text)
        tree = root.xpath('//ul[@class="sch_result_list"]/li')
        titles = [''.join(i.xpath('.//a[@class="tit_txt"]/text()')) for i in tree]
        dates = [i.xpath('.//p[@class="link_dsc_txt dsc_sub"]/span/text()')[0].split()[0].replace('.','-') for i in tree]
        urls = [i.xpath('.//a/@href')[0] for i in tree]
        results = list(zip(urls, titles, dates))
        headers = {'User-Agent':'PostmanRuntime/7.26.8'}
        for iurl, ititle, idate in results:
            yield scrapy.Request(
                url=iurl, 
                headers = headers,
                callback=self.parse,
                meta= {'title':ititle,'url': iurl,'date': idate}
            )
    def parse(self, response):
        post_items = OnlineCommunityCrawlItem()
        title = response.meta['title']
        date = response.meta['date']
        url = response.meta['url']

        root = html.fromstring(response.text)
        contents = ''.join([i for i in root.xpath('//div[@class="write_div"]/*/*/*/text()|//div[@class="write_div"]/*/*/text()|//div[@class="write_div"]/*/text()')])

        vote_up = int(root.xpath('//div[@class="up_num_box"]/p[contains(@class,"up_num font_red")]/text()')[0])
        vote_down = int(root.xpath('//div[@class="down_num_box"]/p[contains(@class,"down_num")]/text()')[0])

        post_items['title'] = title
        post_items['url'] = url
        post_items['date'] = date
        post_items['contents'] = contents
        post_items['vote_up'] = vote_up
        post_items['vote_down'] = vote_down
        post_items['source'] = 'dcinside'
        yield post_items


