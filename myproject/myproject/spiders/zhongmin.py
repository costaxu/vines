#coding: utf-8
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from myproject.items import MyItem
import re, time

class ZhongminSpider(BaseSpider):
    name = 'zhongmin'
    allowed_domains = [
            'zhongmin.cn',
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

    def parse(self, response):
        pass
