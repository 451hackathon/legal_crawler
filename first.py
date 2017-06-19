import scrapy

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['https://blog.scrapinghub.com']

    def start_requests(self):
	yield Request(self.baseUrl + '0')

    def parse(self, response):
	if response.status  != 404:
	        page = response.meta.get('page', 0) + 1
	        return Request('%s%s' % (self.baseUrl, page), meta=dict(page=page))
