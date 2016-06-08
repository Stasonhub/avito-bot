import sys, requests
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

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
        self.stored_list = self.create_item_list()

    def create_item_list(self):
        item_list = {}
        for div in self.parsed_page:
            local_item = item(div)
            item_list[local_item.dict['id']] = local_item.dict
        return item_list

    def check_item_lists(self, new_list):
        mybot = bot()
        if self.stored_list.keys() != new_list.keys():
            for key in new_list.keys():
                if key not in self.stored_list.keys():
                    self.stored_list = new_list
                    return mybot.send_a_message(new_list[key])

class item:
    def __init__(self, div):
        self.dict = {}
        self.div = div
        self.dict['id'] = div.find('a').get('href')
        self.dict['title'] = div.find('a').get_text()
        self.dict['price'] = div.find('div').get_text()
        self.dict['description'] = div.find_all('p')

class bot:
    def __init__(self):
        print ('Hello')

    def send_a_message(self, message):
        print (message)

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
    old_list = db.create_item_list()

    #test 
    db.stored_list.popitem()
    new_list = db.create_item_list()

# example: https://habrahabr.ru/post/302688/

# Q:
# 1. global??
# 2. comparison of two dicts
# 3. method overloading