#!/usr/bin/env python
#coding: utf-8
from myproject.dataframe import DataFrame
d = DataFrame()
def PrintItem(item):
    for key in item.keys():
        if str(type(item[key])) == "<type 'unicode'>":
            item[key] = item[key].encode('utf-8')

    for key in ('category', 'title', 'url', 'brand', 'is_valid', 'domain'):
        if not item.has_key(key) or item[key] is None:
            item[key] = key

    print "%s : %s : %s : %s : %s : %s" % (
            item['category'], 
            item['title'], 
            item['url'], 
            item['brand'], 
            str(item['is_valid']),
            item['domain'],
            )

#for item in d.QueryAll():
#for item in d.BatchQueryByDomain('hzins.com'):
for item in d.BatchQueryByDomain('ubao.com'):
    PrintItem(item)
        
    #if item.has_key('clause_html') and item['clause_html'] == None :#and item['clause_html'].find(u'保障内容') == -1:
    #    print item['title'].encode('utf-8')
    #    print item['url'].encode('utf-8')
#        print item['clause_html'].encode('utf-8')
        
