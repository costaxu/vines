#coding: utf-8
from scrapy.selector import HtmlXPathSelector,XmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from myproject.items import MyItem
import re, time
from datetime import datetime
from insurance_spider import InsuranceSpider


class UbaoSider(InsuranceSpider):
    name = 'ubao'
    domain = u'ubao.com'
    allowed_domains = [
            'ubao.com',
            '172.25.39.114:8080',
    ]
    start_urls = [
            'http://www.ubao.com',
    ]
    rules = (
            Rule(
                SgmlLinkExtractor(
                    allow = ('showPlanDetail'), 
                    deny  = (
                        '-tab', 
                        'prompt'
                    ), 
                 ) 
                ,
                callback = 'parse_item',
            ),
            Rule(
                SgmlLinkExtractor(
                    allow = ('/sp/p\d+'), 
                    deny = ('sp/p\d+[a-z]'),
                ) 
            ),
    )

    product_item_set = set()
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
        title = hxs.select('//h1[@property="v:name"]/text()').extract()
        if title:
            title = title[0]
            title = title.replace('\r\n', '').replace(' ','')
            return title

    def parse_clause_html(self, hxs):
        clause_div = hxs.select("//div[@class='ins-detail clear']")
        if clause_div:
            return clause_div[0].extract()

    def parse_brand(self, hxs):
        brand = hxs.select("//img[@class='hlog']/@alt").extract()
        if brand:
            return brand[0] 
        brand = hxs.select("//div[@class='ins-info']//img/@alt").extract()
        if brand:
            return brand[0]

    def parse_category(self, hxs):
        category = hxs.select("//div[@class='catnav whi']//a/text()").extract()
        if category:
            category = category[0]
            return category
        return u''

    def parse_is_valid(self, hxs):
        return True
