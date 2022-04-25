# WTAReviewScraper
A scrapy webcrawler orginally implemented to scrape hike information and trip report data from WTA's hike website and upload to private mongodb collection for internal use, mainly data processing and data analysis practice.

I rely heavily on the scrapy documentation at docs.scrapy.org. 

The main workhorse of the project is the wta_spider.py in which I extend the scrapy spider class to first scrape the hike data from the website's search results. In this class I follow only two types of links, the next page link and the hike hike page link. I make use of both xpath and css selectors as well as a custom scrapy.Item class and the scrapy.ItemLoader class. After each hike is scraped, it is put through input and output processors defined in my custom HikeItem located in items.py by the scrapy.ItemLoader. Then my pipeline class inserts the item as a dictionary into my mongodb database. The spider proceeds to crawl all hikes listed in the search results by following the next page link.
