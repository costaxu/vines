# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from datetime import datetime
class MyprojectPipeline(object):
    client = pymongo.MongoClient()
    collection = client.mydb.insurance

    def process_item(self, item, spider):
        found = self.collection.find_one({'url' : item['url']})
        if found:
            if found['clause_html'] != item['clause_html']: 
                found['clause_html'] = item['clause_html']
                found['last_modified_time'] = datetime.now()
                self.collection.save(found)
        else:
            item['first_crawled_time'] = datetime.now()
            item['last_modified_time'] = item['first_crawled_time']
            self.collection.insert(dict(item))
        return item
