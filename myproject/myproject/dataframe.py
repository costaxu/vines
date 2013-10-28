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

    def BatchQueryByDomain(self, domain):
        for item in self.collection.find({'domain': domain}):
            yield item
    
    def BatchQuery(self, domain, condition = None):
        for item in self.collection.find(condition):
            yield item

    def QueryKeyWord(self, keyword, limit = (0, 10)):
        if type(keyword) == str:
            keyword = keyword.decode('utf-8')
        item_list = []
        for item in self.collection.find():
            for value in item.values():
                if type(value) == unicode:
                    if value.find(keyword) != -1:
                        item_list.append(item)
        start, length = limit
        end = start + length
        return len(item_list), item_list[start:end]
