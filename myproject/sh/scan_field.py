#!/usr/bin/env python
#coding: utf-8
from myproject.dataframe import DataFrame
from myproject.items import MyItem
d = DataFrame()
def ScanItem(item):
    
    if not item.has_key('url'):
        print 'error item has no url'
        return
    url = item['url']
    time = item['last_crawl_time']
    for key in MyItem.fields.keys():
        if key in ('body'): continue
        if not item.has_key(key) or item[key] is None:
            print url
            print "has no key"
            print key
            print time
            continue
        if type(item[key]) == str or\
                type(item[key]) == unicode:
            if item[key] == '':
                print url
                print "has no string key"
                print key
                print time


#for item in d.QueryAll():
#for item in d.BatchQueryByDomain('hzins.com'):
#for item in d.BatchQueryByDomain('kaixinbao.com'):
for item in d.BatchQueryByDomain('zhongmin.cn'):
    ScanItem(item)

