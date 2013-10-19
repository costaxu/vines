#coding: utf-8
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
import dataframe
class MyprojectPipeline(object):
    data_frame = dataframe.DataFrame()
    def process_item(self, item, spider):
        found = self.data_frame.QueryByUrl(item['url'])
        if found:
            dict_item = dict(item)
            dict_item['_id'] = found['_id']
            if found.has_key('category') and \
                dict_item.has_key('category') and \
                -1 == found['category'].find(dict_item['category']):
                dict_item['category'] = found['category'] + "|" + dict_item['category']
            self.data_frame.Update(dict_item)
        else:
            self.data_frame.Update(item)
        return item
    '''
    def process_item(self, item, spider):
        found = self.data_frame.QueryByUrl(item['url'])
        if found:
            if self.IsItemChanged(found, item):
                #print "**********item changed***************"
                dict_item = dict(item)
                dict_item['_id'] = found['_id']
                dict_item['first_crawled_time'] = found['first_crawled_time']
                
                dict_item['last_modified_time'] = datetime.now()
                self.data_frame.Update(dict_item)
            #else:
                #print "*************item not changed***************"
        else:
            item['first_crawled_time'] = datetime.now()
            item['last_modified_time'] = item['first_crawled_time']
            self.data_frame.Update(item)
        self.data_frame.Update(item)
        return item

    def IsItemChanged(self, saved_item, new_item):
        for key in new_item.keys():
            #新增字段了
            if not saved_item.has_key(key):
                #print "************changed key is %s" % key
                return True

            #字段变化了
            if saved_item[key] != new_item[key]:
                #print type(saved_item[key])
                #print type(new_item[key])
                #print "************changed key is %s" % key
                return True
        return False
   ''' 
