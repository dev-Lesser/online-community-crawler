# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OnlineCommunityCrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    contents = scrapy.Field()
    date = scrapy.Field()
    url = scrapy.Field()
    vote_up = scrapy.Field()
    vote_down = scrapy.Field()
    source = scrapy.Field()
