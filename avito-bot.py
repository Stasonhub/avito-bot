import sys, requests
from bs4 import BeautifulSoup

url = ''
query = ''
old_list = {}

class parser:
    def __init__(self, link):
        self.link = link

    def get_parsed_page(self):
        soup = BeautifulSoup(requests.get(self.link).text, 'html.parser')
        after_ads = soup.find_all('div', {'class': 'js-catalog_after-ads'})
        return after_ads[0].find_all('div', {'class': 'description'})

class db:
    def __init__(self, parsed_page):
        self.parsed_page = parsed_page
        self.stored_list = {}

    def create_item_list(self):
        item_list = {}
        for div in self.parsed_page:
            local_item = item(div)
            item_list[local_item.dict['id']] = local_item .dict
        stored_list = item_list
        return item_list

class item:
    def __init__(self, div):
        self.dict = {}
        self.div = div
        self.dict['id'] = div.find('a').get('href')
        self.dict['title'] = div.find('a').get_text()
        self.dict['price'] = div.find('div').get_text()
        self.dict['description'] = div.find_all('p')
    # def make_item_old():
    #     self.item_new = false

# def get_list():
#     global query
#     items_dict = {}
#     query = query.upper()
#     items = get_items(url)
#     for item in items:
#         title = item.find('a').get_text().upper()
#         if title.find(query) != -1:
#             items_dict[item.find('a').get('href')] = item
#     return items_dict

# def check_lists(old):
#     global old_list
#     new = get_list()
#     if old.keys() != new.keys():
#         print ('lists are not equal')
#     else:
#         print ('nothing new')

# def send_message(message):
#     print (message)

def main():
    global url
    global query
    
    if len(sys.argv) >= 3:
        section = sys.argv[1]
        query = sys.argv[2]
        url = 'https://www.avito.ru/sankt-peterburg/%s?q=%s' % (section, query)

if __name__ == '__main__':
    main()
    parsed_object = parser(url)
    parsed_object = parsed_object.get_parsed_page()
    db = db(parsed_object)
    # db.create_item_list()
    # old_list = get_list()

# example: https://habrahabr.ru/post/302688/

# class source:
# class item:
# class db:
# class bot:


# Q:
# 1. global??
# 2. comparison of two dicts
# 3. method overloading