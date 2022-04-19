import scrapy
import re
from ..items import HikeItem

class wta_spider(scrapy.Spider):
    name='wta_spider'
    start_urls=['https://www.wta.org/go-outside/hikes'] #start_urls is a shortcut for start_requests()

    def parse(self,response):
        i = 0
        for hike_item in response.css('div.search-result-item'): #the parent of all hike item fields
            hike_header = hike_item.css(' div.item-header') #the parent of name, region 1 and region 2 fields
            hike_stats = hike_item.css(' div.hike-stats.alpha > div') #the parent of all the rest of the fields

            hike = HikeItem()
            hike['name'] = hike_header.xpath('.//a/span/text()').get()
            hike['region_1'] = hike_header.xpath('.//h3/text()').get()
            hike['region_2'] = hike_header.xpath('.//h3/text()').get()
            hike['length'] = hike_stats.css('div.hike-length > span::text').get()
            hike['roundtrip'] = hike_stats.css('div.hike-length > span::text').get()
            hike['gain'] = hike_stats.css('div.hike-gain > span::text').get()
            hike['highpoint'] = hike_stats.css('div.hike-highpoint > span::text').get()
            hike['rating'] = hike_stats.css('div.current-rating::text').get()
            hike['votes'] = hike_stats.css('span.rating-count::text').get()
            hike['features'] = hike_stats.css('div.trip-features img::attr(title)').getall()
            hike['desc'] = hike_item.css('div.listing-summary.omega.show-excerpt::text').get()
            yield hike
        next_page = response.css('li.next > a').xpath('./@href').get() #getting next page link
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse) #recursively parsing each page