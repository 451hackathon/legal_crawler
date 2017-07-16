# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import logging

class CensorshipCrawlerPipeline(object):
    def process_item(self, item, spider):
        return item

class ReportSubmissionPipeline(object):


    def __init__(self, collector_url):
        self.logger = logging.getLogger('ReportSubmissionPipeline')
        self.collector_url = collector_url

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            collector_url=crawler.settings.get('COLLECTOR_URL'),
        )

    def open_spider(self, spider):
        from requests_twisted import TwistedRequestsSession
        self.session = TwistedRequestsSession()
        pass

    def close_spider(self, spider):
        self.session.close()
        pass

    def process_item(self, item, spider):
        data = {
                'url': item['url'],
                'creator': 'LegalCrawler',
                'version': '0.0.1',
                'status': int(item['status']),
                'statusText': 'Unavailable for legal reasons',
                'blockedBy': item['blockedBy'],
                'date': item['date']
                }
        self.logger.info("Creating report: %s", json.dumps(data))
        self.session.post(self.collector_url, 
                data=json.dumps(data),
                headers={'Content-type': 'application/json'},
                ).addCallback(self.report_sent)

    def report_sent(self, response):
        self.logger.info("Response sent: {0}", response.status_code)



        

