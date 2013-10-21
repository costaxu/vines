#coding: utf-8
from scrapy.selector import HtmlXPathSelector,XmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from myproject.items import MyItem
import re, time
from datetime import datetime
from insurance_spider import InsuranceSpider

class HuizeSpider(InsuranceSpider):
    name = 'huize'
    domain = u'hzins.com'
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
                ),
                callback='parse_item',
            ),
            Rule(
                SgmlLinkExtractor(
                    #deny = (
                    #    'http.*pdf$',
                    #    #旅游险
                    #    'product/ins-21',
                    #    'www.hzins.com/study/',
                    #    'www.hzins.com/content-',
                    #),
                    allow = (
                        'product/ins-[0-9]*-0-0',
                        'content-[0-9]*-0-1_0-0-[0-9]*-0',
                        ),
                ),
                callback='parse_links',
            ),
    )

    def parse_links(self, response):
        url_prefix = '/'.join(response.url.split('/')[0:3])
        xxs = XmlXPathSelector(response)
        xxs.remove_namespaces()
        selects = xxs.select("//a/@hz-location").extract()
        for hz_location in selects:
            #print "find request %s" % hz_location
            yield Request(url = url_prefix + hz_location, method="POST", 
                    body="X-Requested-With=XMLHttpRequest",
                    headers = {
                        "Accept-Encoding": "gzip, deflate",
                        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
                        "X-Requested-With": "XMLHttpRequest",
                        "Accept": "*/*",
                    }
                    ) 

    def parse_item(self, response, **kwargs):
        #t1  = time.time()
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
        title = hxs.select('//h1[@class="w_limit"]/text()').extract()
        if title:
            title = title[0]
            title = title.replace('\r\n', '').replace(' ','')
            return title

    def parse_clause_html(self, hxs):
        clause_div = hxs.select("//div[@class='sf_project_ttab']|//table[@class='a_text']")
        if clause_div:
            return clause_div[0].extract()
        else:
            tables = hxs.select('//div[@class="Sth_cont1"]/table').extract()  
            for table in tables:
                if table.find("产品名称".decode("utf-8")) != -1:
                    return table

    def parse_brand(self, hxs):
        brand = hxs.select("//div[@class='public_current']/a/text()").extract()
        if brand:
            brand = brand[-1]
            return brand 
        return u''

    def parse_category(self, hxs):
        category = hxs.select("//div[@class='public_current']/a/text()").extract()
        if category:
            category = category[-2]
            return category
        return u''

    def parse_is_valid(self, hxs):
        stop_sale = hxs.select("//input[@id='hfPublish']/@value").re("Stop")
        if stop_sale: return False
        else: return True
