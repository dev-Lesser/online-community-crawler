import scrapy


class IlbeSpider(scrapy.Spider):
    name = 'ilbe'
    allowed_domains = ['https://www.ilbe.com']
    start_urls = ['http://https://www.ilbe.com/']

    def parse(self, response):
        result = []
        date = []
        # for i in tqdm(range(1,10)):
        page_num = 1
        url = 'https://www.ilbe.com/search?docType=doc&searchType=title_content&page={page_num}&q=이준석'.format(page_num=1)
        res = requests.get(url)
        root = html.fromstring(res.text)
        tree = root.xpath('//div[@class="search-list"]/ul/li')
        #     [''.join(i.xpath('.//a/text()')).replace('\xa0','') for i in tree]
        result += [''.join(i.xpath('.//a/text()|.//a/strong/text()')) for i in tree]
        date += [i.xpath('.//span[@class="date"]/text()')[0].split()[0] for i in tree]

