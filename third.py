import scrapy

class MySpider(scrapy.Spider):
    name = 'afrinic.net'
    baseUrl = "http://afrinic.net"
    handle_httpstatus_list = [404]

    def parse(self, response):
        if response.status != 404:
            page = response.meta.get('page', 0) + 1
            return Request('%s%s' % (self.baseUrl, page), meta=dict(page=page))
