#coding: utf-8
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from myproject.items import MyItem
import re, time
from hz_icon import hz_brand_icon_map

class HuizeSpider(BaseSpider):
    name = 'huize'
    allowed_domains = [
            'hzins.com',
            #for test
            '172.25.39.114:8080',
            ]
    start_urls = [
            #'http://www.hzins.com/',
            'http://www.hzins.com/product/ins-19-0-0',
            #'http://www.hzins.com/sitemap.xml',
            ]
    useless_url_patterns = [
            'http.%pdf$',
            #旅游险
            'http://www.hzins.com/product/ins-21',
            'http://www.hzins.com/study/',
            ]
    useless_url_regexes = []
    for useless_url_pattern in useless_url_patterns:
        useless_url_regex = re.compile(useless_url_pattern)
        useless_url_regexes.append(useless_url_regex)
    crawled_url_count = 0
    crawled_url_set = set()
        
    def parse(self, response):
        #t1  = time.time()
        hxs = HtmlXPathSelector(response)
        
        url = response.url
        if url not in self.crawled_url_set:
            
            url_prefix = '/'.join(url.split('/')[0:3])
            title = self.parse_title(hxs)
            clause_html = self.parse_clause_html(hxs)
            brand = self.parse_brand(hxs)
            if title:
                yield MyItem(title = title, url = url, clause_html = clause_html, brand = brand)
            href_list = []    
            for href in hxs.select('//loc/text()'):
                href_list.append(href)

            for href in hxs.select('//a/@href'):
                href_list.append(href)

            for href in hxs.select('//a/@hz-location'):
                href_list.append(href)

            for href in href_list:
                url = href.extract()
                if not url.startswith('http'):
                    url = url_prefix + url
                #self.log("useless pattern len %d" % len(MySpider.useless_url_regexes))   
                useless = False

                if url in self.crawled_url_set:
                    useless = True
                    break

                for useless_url_regex in self.useless_url_regexes:
                    #self.log("Find url %s" % url)
                    if useless_url_regex.match(url): 
                        self.log('url match useless pattern ')
                        useless = True
                        break
                if not useless:        
                    yield Request(url.rstrip('\r\n'), callback = self.parse)
            self.crawled_url_set.add(url)
            self.crawled_url_count += 1
            if self.crawled_url_count % 1000 == 0:
                self.log("Crawled Url Count = %d" % (self.crawled_url_count))

        #t2 = time.time()
        #self.log("Parse %s use time %f s" % (url, t2 - t1))

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
