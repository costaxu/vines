# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class MyItem(Item):
    # define the fields for your item here like:
    # name = Field()
    title = Field()
    url = Field()
    body = Field()
    clause_html = Field()
    brand = Field()
    #first_crawled_time = Field()
    #last_modified_time = Field()
    is_valid = Field()
    domain = Field()
    category = Field()
    last_crawl_time = Field()

    def __repr__(self):
        return self.title
    
