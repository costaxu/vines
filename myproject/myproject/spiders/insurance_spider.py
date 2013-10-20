#coding: utf-8
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from myproject.dataframe import DataFrame

class InsuranceSpider(CrawlSpider):
    domain = u''
    def start_requests(self):
        data_frame = DataFrame()
        for item in data_frame.BatchQueryByDomain(self.domain):
            self.log("####################start url %s" % item['url'])
            yield Request(url = item['url'])

