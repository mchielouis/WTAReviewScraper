import scrapy
import re
from ..items import HikeItem, remove_whitespace, str_to_int, str_to_float
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, Identity

# A class for crawling the wta website to collect hike data and hike reports.
class wta_spider(scrapy.Spider):
    name = 'wta_spider'
    start_urls = ['https://www.wta.org/go-outside/hikes']  # start_urls is a shortcut for start_requests()

    # Parses the hike data from search result items into HikeItems using scrapy.ItemLoader.
    def parse(self, response):
        i = 0
        for hike_search_result_sel in response.css('div.search-result-item'):  # the parent selector of all hike hike item fields

            hike = HikeItem()  # my custom hike item
            l = ItemLoader(hike, selector=hike_search_result_sel)  # item loader

            # Most field data I feed through the hike item's input and output processors, but name is simple enough
            # to get directly without processing.
            hike['name'] = l.get_xpath('.//a/span/text()', TakeFirst())  # name
            l.add_xpath('region_1', './/h3/text()')  # region_1
            l.add_xpath('region_2', './/h3/text()')  # region_2
            l.add_css('gain', 'div.hike-gain > span::text')  # gain
            l.add_css('highpoint', 'div.hike-highpoint > span::text')  # highpoint
            l.add_css('length', 'div.hike-length > span::text')  # length
            l.add_css('roundtrip', 'div.hike-length > span::text')  # roundtrip
            l.add_css('rating', 'div.current-rating::text')
            l.add_css('votes', 'span.rating-count::text')
            l.add_css('features', 'div.trip-features img::attr(title)')
            l.add_css('desc', 'div.listing-summary.omega.show-excerpt::text')

            # Follow link to hike page to collect coordinate data.
            hike_page = hike_search_result_sel.css(' a::attr(href)').get()
            if hike_page:
                yield scrapy.Request(hike_page, callback=self.parse_hike_page, meta={'item': l.load_item()})

        # The spider will crawl through all pages of search results.
        next_page = response.css('li.next > a').xpath('./@href').get()  # getting next page link
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)  # recursively parsing each page
    # On the hike page, we instatiate a new itemloader but continue using same item instance (passed in repsonse meta)
    def parse_hike_page(self, response):
        l_hike_page = ItemLoader(item=response.meta['item'], response=response)
        l_hike_page.add_css('coords', 'div.latlong span::text')
        yield l_hike_page.load_item()