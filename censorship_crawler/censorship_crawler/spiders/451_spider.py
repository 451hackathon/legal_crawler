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

from scrapy.linkextractors import LinkExtractor

class CensorshipSpider(scrapy.Spider):
    name = "451"
    
    def __init__(self, *args, **kw):
        self.regexp = '.*' # default value for regexp filter
        super(CensorshipSpider, self).__init__(*args, **kw)

        # create an extractor that only returns urls matching a regexp
        self.extractor = LinkExtractor(allow=self.regexp)

    def start_requests(self):
        if hasattr(self, 'url'):
            urls = [self.url]
        else:
            urls = [
                'http://www.newzbin.com/',
                'http://www.hackers.mu/',
            ]
        for url in urls:
            yield scrapy.Request(url=url)

    def record_451(self, response):
        report = {
                'url': 'base64:' + response.url.encode('base64').strip(),
                'creator': 'CensorshipCrawler',
                'version': '0.0.1',
                'status': response.status,
                'statusText': 'Unavailable for Legal Reasons',
                }

        if 'Link' in response.headers:
            link = response.headers['Link']
            if 'rel=' in link and 'blocked-by' in link:
                report['blockedBy'] = link.split('; ')[0].strip('<>')

        self.log(report)
        with open('output.json', 'a') as fp:
            fp.write(json.dumps(report)+"\n")

        # TODO: send to central collector

    def parse(self, response):
        if response.status == 451:
            self.record_451(response)
        else:

            # extract links for further items
            for link in self.extractor.extract_links(response):
                print link
                yield scrapy.Request(url=link.url)



