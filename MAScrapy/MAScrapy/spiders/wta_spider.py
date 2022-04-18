import scrapy

class wta_spider(scrapy.Spider):
    name='wta_spider'
    start_urls=['https://www.wta.org/go-outside/hikes'] #start_urls is a shortcut for start_requests()

    def parse(self,response):
        for hike_header in response.css('div.item-header'): #looping over hike item blocks
            try:
                yield {
                    'HIKE_NAME': hike_header.xpath('.//a/span/text()').get(),
                    'REGION_1': hike_header.xpath('.//h3/text()').get().rsplit('--')[0].strip(),
                    'REGION_2': hike_header.xpath('.//h3/text()').get().rsplit('--')[1].strip()
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