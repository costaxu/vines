#coding: utf-8
import web
from myproject import dataframe

urls = (
        '/', 'index'
        )
dfo = dataframe.DataFrame()
ITEM_PER_PAGE = 10

class index:
    def GET(self):
        render = web.template.render('templates/')
        data = web.input(w='', p='1')
        keyword = data.w
        current_page = int(data.p)
        if not keyword:
            return render.index(length= None, 
                    item_list = None, 
                    current_page = None,
                    total_page = None,
                    keyword = None)
        limit_start = (current_page - 1) * ITEM_PER_PAGE
        limit_len = ITEM_PER_PAGE
        limit = limit_start, limit_len
        length, item_list = dfo.QueryKeyWord(keyword, limit = limit)
        total_page = length / ITEM_PER_PAGE 
        if length % ITEM_PER_PAGE :
            total_page += 1
        return render.index(length= length, 
                item_list = item_list, 
                current_page = current_page, 
                total_page = total_page,
                keyword = keyword)
        

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
