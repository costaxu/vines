#coding: utf-8
import pymongo

DB_NAME='spider_db'
COLLECTION_NAME = "insurance"

class DataFrame:
    client = pymongo.MongoClient()
    collection = client[DB_NAME][COLLECTION_NAME]

    def Insert(self,item):
        self.collection.insert(dict(item))

    def QueryByUrl(self, url):
        found = self.collection.find_one({'url': url})
        if found:
            return found
        else:
            return None

    def Update(self, item):
        self.collection.save(dict(item))

    def QueryAll(self):
        item_list = []
        for item in self.collection.find():
            item_list.append(item)
        return item_list
