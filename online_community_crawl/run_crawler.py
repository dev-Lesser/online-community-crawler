from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def scrapy_run(spider_name):
    process = CrawlerProcess(get_project_settings())
    process.crawl(spider_name) # set crawler name

    process.start()

if __name__ == '__main__':

    scrapy_run('ilbe')
    scrapy_run('dcinside')
    scrapy_run('mlbpark')
    scrapy_run('inven')
    scrapy_run('ppomppu')
    scrapy_run('clien')