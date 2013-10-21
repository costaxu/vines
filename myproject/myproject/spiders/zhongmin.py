#coding: utf-8
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from myproject.items import MyItem
from insurance_spider import InsuranceSpider
import re, time, json
from datetime import datetime

TRAVEL_PAGE_URL = "http://www.zhongmin.cn/TravelAsy.asmx/TravelList"
class ItemParser:
    def ParseTitle(self, hxs):
        title = hxs.select('//span[@class="cp_tit"]/text()').extract()
        if title:
            title = title[0]
            title = title.replace('\r\n', '').replace(' ','')
            return title

    def ParseClauseHtml(self, hxs):
        clause_div = hxs.select("//div[@class='xxk']")
        if clause_div:
            return clause_div.extract()

    def ParseBrand(self, hxs):
        brand = hxs.select('//div[@class="mycx_wz"]/a/text()').extract()
        if brand:
            return brand[0].replace('\r\n', '').replace(' ','')

    def ParseCategory(self, hxs):
        category = hxs.select("//div[@class='szwz']/a/text()").extract()
        if category:
            category = category[-2]
            return category.replace('\r\n', '').replace(' ','')
        return u''

class ZhongminSpider(CrawlSpider):
    name = u'zhongmin'
    domain = u'zhongmin.cn'
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
                allow = (
                    'Travel/Product/Travel.*html',
                    'ProductDetails.aspx',
                    ), 

                ),
            callback = "parse_travel_item",
        ), 
        Rule(
            SgmlLinkExtractor(
                allow = ("www.zhongmin.cn/TravelAsy.asmx"), 
            ),
            callback = "parse_page_url",
        ),
        Rule(
            SgmlLinkExtractor(
               allow = ("www.zhongmin.cn/Travel"), 
            ),   
            callback = "parse_pages",
        ),
    
    )

    def parse_pages(self, response):
        hxs = HtmlXPathSelector(response)
        page_count = hxs.select("//div[@id='pager1']/b/text()").extract()
        if page_count:
            page_count = int(page_count[0])
            self.log("Parse %d pages from %s" % (page_count, response.url))
            for i in range(1, page_count + 1):
                yield Request(url = TRAVEL_PAGE_URL, 
                        method = "POST", 
                        body = "age=-1&day=1&safe=-1&com=-1&area=-1&order=0&field=0&page=%d&type=0" % i,
                        headers = {
                            "Accept-Encoding": "gzip, deflate",
                            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
                            "X-Requested-With": "XMLHttpRequest",
                            "Accept": "*/*",    
                        })

    def parse_page_url(self, response):
        self.log("###############Parse_page_url")
        xxs = XmlXPathSelector(response)
        xxs.remove_namespaces()
        json_object = json.loads(xxs.select("//string/text()").extract()[0])
        for product in json_object['product']:
            if product['isYuyue'] == 'True':
                url = 'http://www.zhongmin.cn/Product/ProductDetails.aspx?pid=%s&bid=11' % product['Id']
            else:
                url = 'http://www.zhongmin.cn/Travel/Product/TravelDetailArr%(Id)s-%(age)sd%(day)s.html' % product
            yield Request(url = url)

    def parse_travel_item(self, response):
        self.log("********************************************parse_item*************************************** %s " % (response.url))
        hxs = HtmlXPathSelector(response)
        item_parser = ItemParser()
        url = response.url
        body = hxs.select("/html/body").extract()
        title = item_parser.ParseTitle(hxs)
        clause_html = item_parser.ParseClauseHtml(hxs)
        brand = item_parser.ParseBrand(hxs)
        category = item_parser.ParseCategory(hxs)
        last_crawl_time = datetime.now()
        if title:
            yield MyItem(title = title, 
                    #body = body,
                    url = url, 
                    clause_html = clause_html, 
                    brand = brand, 
                    domain = self.domain,
                    category = category,
                    is_valid = True,
                    last_crawl_time = last_crawl_time)
