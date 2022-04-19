# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HikeItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    region_1 = scrapy.Field()
    region_2 = scrapy.Field()
    length = scrapy.Field()
    gain = scrapy.Field()
    highpoint = scrapy.Field()
    roundtrip = scrapy.Field()
    features = scrapy.Field()
    rating = scrapy.Field()
    votes = scrapy.Field()
    desc = scrapy.Field()
    pass
