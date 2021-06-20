"""
펨코의 경우 URL 차단이 좀 심함 : 딜레이를 많이 줘야 할 듯
"""

import scrapy
from lxml import html
from online_community_crawl.items import OnlineCommunityCrawlItem


class FmkoreaSpider(scrapy.Spider):
    name = 'fmkorea'

    def start_requests(self):
        # for page_num in range(100)
        urls = ['https://www.fmkorea.com/index.php?act=IS&is_keyword=이준석&mid=home&where=document&page={page_num}'.format(page_num=i) for i in range(1,300)] # 시간순 정렬 되어 있음
        for iurl in urls:
            yield scrapy.Request(
                url=iurl, 
                callback=self.parse_url
            )
    def parse_url(self, response):

        root = html.fromstring(response.text)
        tree = root.xpath('//ul[@class="searchResult"]/li')
        titles = [''.join(i.xpath('.//dl/dt/a/text()')).replace('[정치/시사] ','') for i in tree] # 정치/시사 라는 타이틀제목에 붙는 prefix 제거
        dates = [i.xpath('.//address/span[@class="time"]/text()')[0].split()[0] for i in tree]
        urls = [''.join(i.xpath('.//dl/dt/a/@href')) for i in tree]
        results = list(zip(urls, titles, dates))
        for iurl, ititle, idate in results:
            yield scrapy.Request(
                url='https://www.fmkorea.com/'+iurl, 
                callback=self.parse,
                meta= {'title':ititle,'url': iurl,'date': idate}
            )
    def parse(self, response):
        post_items = OnlineCommunityCrawlItem()
        title = response.meta['title']
        date = response.meta['date']
        url = response.meta['url']

        root = html.fromstring(response.text)
        contents = ' '.join(root.xpath('//article/div/*/text()')).replace(u'\xa0',u' ')

        vote_up = int(root.xpath('//span[@class="vote"]/span/text()')[0]) # 펨코의 경우 마이너스의 집계는 안보여줌
        vote_down = 0

        post_items['title'] = title
        post_items['url'] = url
        post_items['date'] = date
        post_items['contents'] = contents
        post_items['vote_up'] = vote_up
        post_items['vote_down'] = vote_down
        post_items['source'] = 'fmkorea'
        yield post_items


