#coding: utf-8
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from myproject.items import MyItem
import re, time
from hz_icon import hz_brand_icon_map

class HuizeCrawlSpider(CrawlSpider):
    name = 'huizetest'
    allowed_domains = [
            'hzins.com',
            #for test
            '172.25.39.114:8080',
    ]
    start_urls = [
            'http://www.hzins.com/',
            #'http://www.hzins.com/product/ins-19-0-0',
            #'http://www.hzins.com/product/travel/detal-135.html',
            #'http://www.hzins.com/sitemap.xml',
    ]
    rules = (
            Rule(
                SgmlLinkExtractor(
                    allow=('product.*det',),
                    attrs = ('href', 'hz-location'),
                ),
                callback='parse_item',
            ),
            Rule(
                SgmlLinkExtractor(
                    deny = (
                        'http.*pdf$',
                        #旅游险
                        'product/ins-21',
                        'www.hzins.com/study/',
                        'www.hzins.com/content-',
                    ),
                    attrs = ('href', 'hz-location'),
                )
            ),
    )
    def parse_item(self, response):
        #t1  = time.time()
        self.log("********************************************parse_item*************************************** %s " % (response.url))
        hxs = HtmlXPathSelector(response)
        
        url = response.url
        title = self.parse_title(hxs)
        clause_html = self.parse_clause_html(hxs)
        brand = self.parse_brand(hxs)
        if title:
            yield MyItem(title = title, url = url, clause_html = clause_html, brand = brand)

    def parse_title(self, hxs):
        title = hxs.select('//h1[@class="w_limit"]/text()').extract()
        if title:
            title = title[0]
            title = title.replace('\r\n', '').replace(' ','')
            return title

    def parse_clause_html(self, hxs):
        clause_div = hxs.select("//div[@class='sf_project_ttab']|//table[@class='a_text']")
        if clause_div:
            return clause_div[0].extract()

    def parse_brand(self, hxs):
        brand_icon_url_list = hxs.select('//div[@class="bf_calculatett_1"]/a/img/@src').extract()
        if not brand_icon_url_list :
            return None 
        brand_icon_url = brand_icon_url_list[0]
        if hz_brand_icon_map.has_key(brand_icon_url):
            return hz_brand_icon_map[brand_icon_url]
        else:
            return None
