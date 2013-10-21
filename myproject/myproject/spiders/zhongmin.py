#coding: utf-8
from scrapy.selector import HtmlXPathSelector, XmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from scrapy import log
from myproject.items import MyItem
import re, time, json
from datetime import datetime

TRAVEL_TURN_PAGE_URL = "http://www.zhongmin.cn/TravelAsy.asmx/TravelList"
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

class UrlMatch:
    def __init__(self, patterns, callback):
        self.m_patterns = patterns
        self.m_callback = callback

    def match(self, response):
        matched = False
        for pattern in self.m_patterns:
            if re.search(pattern, response.url):
                log.msg("pattern matched %s %s" % (pattern, response.url))
                matched = True
                break
        if matched:
            return self.m_callback(response)

    
class TurnPageExtractor:
    def matches(self, url):
        return True

        

class ZhongminSpider(BaseSpider):
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
    
    url_matches = (
        UrlMatch(
            patterns = [
                    'Travel/Product/Travel.*html',
                    'ProductDetails.aspx',
                    ], 
            callback = "parse_travel_item",
        ), 
        UrlMatch(
            patterns = ['TravelAsy'],
            callback = "parse_travel_asy",
        ),
        UrlMatch(
            patterns = ['www.zhongmin.cn/Travel/'],
            callback = "parse_index",
        )
    )
    crawled_url_set = set()
    link_extractor = SgmlLinkExtractor()

    def __init__(self, *a, **kw):
        super(ZhongminSpider, self).__init__(*a, **kw)
        self._compile_url_matches()

    def parse(self, response):
        links = self.link_extractor.extract_links(response) 
        for link in links:
            if link.url not in self.crawled_url_set:
                self.crawled_url_set.add(link.url)
                yield(Request(url = link.url))
        for url_match in self.url_matches:
            requests = url_match.match(response)
            if requests:
                for request_or_item in requests:
                    yield request_or_item

    def parse_travel_asy(self, response):
        xxs = XmlXPathSelector(response)
        xxs.remove_namespaces()
        json_object = json.loads(xxs.select("//string/text()").extract()[0])
        request_list = []
        for product in json_object['product']:
            if product['isYuyue'] == 'True':
                url = 'http://www.zhongmin.cn/Product/ProductDetails.aspx?pid=%s&bid=11' % product['Id']
            else:
                url = 'http://www.zhongmin.cn/Travel/Product/TravelDetailArr%(Id)s-%(age)sd%(day)s.html' % product
            request_list.append(Request(url = url))
        return request_list
    
    def parse_index(self, response):
        hxs = HtmlXPathSelector(response)
        page_count = hxs.select("//div[@id='pager1']/b/text()").extract()
        if page_count:
            page_count = int(page_count[0])
            request_list = []
            #self.log("Parse %d pages from %s" % (page_count, response.url))
            for i in range(1, page_count + 1):
                request_list.append(Request(url = TRAVEL_TURN_PAGE_URL, 
                        method = "POST", 
                        body = "age=-1&day=1&safe=-1&com=-1&area=-1&order=0&field=0&page=%d&type=0" % i,
                        headers = {
                            "Accept-Encoding": "gzip, deflate",
                            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
                            "X-Requested-With": "XMLHttpRequest",
                            "Accept": "*/*",    
                        }))
            return request_list

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

    def _compile_url_matches(self):
        def get_method(method):
            if callable(method):return method
            else:
                return getattr(self, method, None)
        for url_match in self.url_matches:
            url_match.m_callback = get_method(url_match.m_callback)

