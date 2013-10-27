#coding: utf-8
from scrapy.selector import HtmlXPathSelector,XmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from myproject.items import MyItem
import re, time
from datetime import datetime
from insurance_spider import InsuranceSpider

BRAND = '泰康人寿'.decode('utf-8')

class TaikangSpider(InsuranceSpider):
    name = 'taikang'
    domain = u'taikang.com'
    allowed_domains = [
            'taikang.com',
            '172.25.39.114:8080',
    ]
    start_urls = [
            'http://shop.taikang.com',
    ]
    rules = (
            Rule(
                SgmlLinkExtractor(
                    allow = ('shop.taikang.com/\w+/\w+'), 
                 ) 
                ,
                callback = 'parse_item',
            ),
            Rule(
                SgmlLinkExtractor(
                    allow = ('shop.taikang.com/\w+'), 
                    deny = ('gallery'),
                ) 
            ),
    )

    def parse_title(self, hxs):
        title = hxs.select('//span[@class="goodsname-con"]/text()').extract()
        if title:
            title = title[0]
            title = title.replace('\r\n', '').replace(' ','')
            return title

    def parse_clause_html(self, hxs):
        clause_div = hxs.select("//ul[@class='tball_info2']")
        if clause_div:
            return clause_div[0].extract()
        clause_div = hxs.select("//div[@class='acc_left_content']")
        if clause_div:
            return clause_div[0].extract()

    def parse_brand(self, hxs):
        return BRAND

    def parse_category(self, hxs):
        category = hxs.select("//div[@class='Navigation']//a/text()").extract()
        if category:
            category = category[-1]
            return category
        return u''

    def parse_is_valid(self, hxs):
        return True
