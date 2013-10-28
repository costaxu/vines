#coding: utf-8
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector,XmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from myproject.items import MyItem
from myproject.dataframe import DataFrame
import re, time
from datetime import datetime

class InsuranceSpider(CrawlSpider):
    domain = u''
    start_urls = []
    def start_requests(self):
        data_frame = DataFrame()
        for url in self.start_urls:
            yield Request(url = url)
        for item in data_frame.BatchQueryByDomain(self.domain):
            self.log("####################start url %s" % item['url'])
            yield Request(url = item['url'], callback = self.parse_item)

    def parse_item(self, response):
        self.log("********************************************parse_item*************************************** %s " % (response.url))
        hxs = HtmlXPathSelector(response)
        url = response.url
        body = hxs.select("/html/body").extract()
        title = self.parse_title(hxs)
        clause_html = self.parse_clause_html(hxs)
        brand = self.parse_brand(hxs)
        category = self.parse_category(hxs)
        is_valid = self.parse_is_valid(hxs)
        last_crawl_time = datetime.now()
        if title:
            yield MyItem(title = title, 
                    #body = body,
                    url = url, 
                    clause_html = clause_html, 
                    brand = brand, 
                    domain = self.domain,
                    category = category,
                    is_valid = is_valid,
                    last_crawl_time = last_crawl_time,
                    )

    def parse_title(self, hxs):
        return ''

    def parse_clause_html(self, hxs):
        return '' 

    def parse_brand(self, hxs):
        return '' 

    def parse_category(self, hxs):
        return '' 

    def parse_is_valid(self, hxs):
        return True
