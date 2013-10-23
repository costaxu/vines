#coding: utf-8
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from myproject.dataframe import DataFrame

class InsuranceSpider(CrawlSpider):
    domain = u''
    start_urls = []
    def start_requests(self):
        data_frame = DataFrame()
        for url in self.start_urls:
            yield Request(url = url)
        for item in data_frame.BatchQueryByDomain(self.domain):
            self.log("####################start url %s" % item['url'])
            yield Request(url = item['url'])

