#
#
# Copyright (c) 2017 Loganaden Velvindron <logan@hackers.mu>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

#Developed for IETF 99 Hackathon

import json
import scrapy
from censorship_crawler.items import CensorshipCrawlerItem

class CensorshipSpider(scrapy.Spider):
    name = "451"
    handle_httpstatus_list = [451]

    def start_requests(self):
        if hasattr(self, 'url'):
            urls = [self.url]
        else:
            urls = [
                'http://www.newzbin.com/',
                'http://www.hackers.mu/',
            ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        report = CensorshipCrawlerItem(url=response.url.encode('base64').strip(),status=response.status)
        if 'Link' in response.headers:
            link = response.headers['Link']
            if 'rel=' in link and 'blocked-by' in link:
                report['blockedBy'] = link.split('; ')[0].strip('<>')
        self.log(report)
        yield report

        # TODO: send to central collector
