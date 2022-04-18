import scrapy

class wta_spider(scrapy.Spider):
    name='wta_spider'
    start_urls=['https://www.wta.org/go-outside/hikes']

    def parse(self,response):
        for hike_header in response.css('div.item-header'):
            yield {
                'HIKE_NAME': hike_header.xpath('.//a/span/text()').get(),
                'REGION_1': hike_header.xpath('.//h3/text()').get().rsplit('--')[0].strip(),
                'REGION_2': hike_header.xpath('.//h3/text()').get().rsplit('--')[1].strip()
            }
