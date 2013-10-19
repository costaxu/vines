#coding: utf-8
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from myproject.items import MyItem
import re, time

class ItemParser:
    def ParseTitle(self, hxs):
        title = hxs.select('//h1[@class="w_limit"]/text()').extract()
        if title:
            title = title[0]
            title = title.replace('\r\n', '').replace(' ','')
            return title

    def ParseClauseHtml(self, hxs):
        clause_div = hxs.select("//div[@class='sf_project_ttab']|//table[@class='a_text']")
        if clause_div:
            return clause_div[0].extract()

    def ParseBrand(self, hxs):
        brand_icon_url_list = hxs.select('//div[@class="bf_calculatett_1"]/a/img/@src').extract()
        if not brand_icon_url_list :
            return None 
        brand_icon_url = brand_icon_url_list[0]
        if hz_brand_icon_map.has_key(brand_icon_url):
            return hz_brand_icon_map[brand_icon_url].decode('utf-8')
        else:
            return None

    def ParseCategory(self, hxs):
        category = hxs.select("//div[@class='public_current']/a/text()").extract()
        if category:
            category = category[-2]
            return category
        return u''


class ZhongminSpider(CrawlSpider):
    name = 'zhongmin'
    allowed_domains = [
            'zhongmin.cn',
            #for test
            '172.25.39.114:8080',
            ]
    start_urls = [
            'http://www.zhongmin.cn/Travel/',
            ]
    
    rules = (
        Rule(
            SgmlLinkExtractor(
                allow = ('Travel/Product/travel.*html'), 
                ),
            callback = parse_travel_item
        ),      
    )
    def parse_travel_item(self, response):
        self.log("********************************************parse_item*************************************** %s " % (response.url))
        hxs = HtmlXPathSelector(response)
        item_parser = ItemParser()
        url = response.url
        body = hxs.select("/html/body").extract()
        title = item_parser.ParseTitle(hxs)
        clause_html = item_parser.ParseClauseHtml(hxs)
        brand = item_parser.ParseBrand(hxs)
        category = self.ParseCategory(hxs)
        if title:
            yield MyItem(title = title, 
                    #body = body,
                    url = url, 
                    clause_html = clause_html, 
                    brand = brand, 
                    domain = self.domain,
                    category = category)
