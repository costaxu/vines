#coding: utf-8
from scrapy.selector import HtmlXPathSelector,XmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from myproject.items import MyItem
import re, time
from datetime import datetime
from insurance_spider import InsuranceSpider


class KaixinbaoSider(InsuranceSpider):
    name = 'kaixinbao'
    domain = u'kaixinbao.com'
    allowed_domains = [
            'kaixinbao.com',
            '172.25.39.114:8080',
    ]
    start_urls = [
            'http://www.kaixinbao.com',
    ]
    rules = (
            Rule(
                SgmlLinkExtractor(
                    allow = ('/\d+\.shtml'), 
                 ) 
                ,
                callback = 'parse_item',
            ),
            Rule(
                SgmlLinkExtractor(
                    allow = ('baoxian', 'index'), 
                ), 
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
        title = hxs.select('//div[@class="cp_titile_con"]/h1/text()').extract()
        if title:
            title = title[0]
            title = title.replace('\r\n', '').replace(' ','')
            return title

    def parse_clause_html(self, hxs):
        clause_div = hxs.select("//div[@class='bzzz_boxtable']/table")
        if clause_div:
            return clause_div[0].extract()

    def parse_brand(self, hxs):
        brands = hxs.select("//div[@class='cp_gscon']/text()").extract()
        for brand in brands:
            brand = brand.strip('\r\n\t ')
            if brand:
                return brand

    def parse_category(self, hxs):
        category = hxs.select("//div[@class='daohang']//a/text()").extract()
        if category:
            category = category[-1]
            return category
        return u''

    def parse_is_valid(self, hxs):
        return True
