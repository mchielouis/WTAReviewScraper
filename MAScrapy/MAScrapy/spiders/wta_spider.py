import scrapy
import re

class wta_spider(scrapy.Spider):
    name='wta_spider'
    start_urls=['https://www.wta.org/go-outside/hikes'] #start_urls is a shortcut for start_requests()

    def parse(self,response):
        i = 0
        for hike_item in response.css('div.search-result-item'): #looping over hike item blocks
            hike_header = hike_item.css(' div.item-header')
            hike_stats = hike_item.css(' div.hike-stats.alpha > div')
            i += 1
            try:
                yield {
                    'ID': i,
                    'HIKE_NAME': hike_header.xpath('.//a/span/text()').get(),
                    'REGION_1': hike_header.xpath('.//h3/text()').get().rsplit('--')[0].strip(),
                    'REGION_2': hike_header.xpath('.//h3/text()').get().rsplit('--')[1].strip(),
                    'LENGTH': float(hike_stats.css('div.hike-length > span::text').get().rsplit(',')[0].split(' ')[0]),
                    'ROUNDTRIP': True if hike_stats.css('div.hike-length > span::text').get().rsplit(',')[1].strip() == 'roundtrip' else False,
                    'GAIN': int(hike_stats.css('div.hike-gain > span::text').get().rsplit(' ')[0]),
                    'HIGHPOINT': int(hike_stats.css('div.hike-highpoint > span::text').get().rsplit(' ')[0]),
                    'RATING': float(hike_stats.css('div.current-rating::text').get()),
                    'VOTES': int(re.findall(r'\d+',hike_stats.css('span.rating-count::text').get())[0]),
                    'FEATURES': hike_stats.css('div.trip-features img::attr(title)').getall(),
                    'DESC': re.sub('(\u2018|\u2019)',"'",hike_item.css('div.listing-summary.omega.show-excerpt::text').get().strip())
                }
            except IndexError:
                yield {
                    'HIKE_NAME': hike_header.xpath('.//a/span/text()').get(),
                    'REGION_1': hike_header.xpath('.//h3/text()').get().rsplit('--')[0].strip(),
                    'REGION_2': ''
                }
        next_page = response.css('li.next > a').xpath('./@href').get() #getting next page link
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse) #recursively parsing each page