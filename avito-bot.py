import sys, requests, config
from bs4 import BeautifulSoup

url = ''
query = ''

class parser:
    def __init__(self, link):
        self.link = link
        self.page = self.get_parsed_page()

    def get_parsed_page(self):
        soup = BeautifulSoup(requests.get(self.link).text, 'html.parser')
        after_ads = soup.find_all('div', {'class': 'js-catalog_after-ads'})
        return after_ads[0].find_all('div', {'class': 'description'})

class db:
    def __init__(self, parsed_page):
        self.parsed_page = parsed_page
        self.stored_list = self.create_item_list(self.parsed_page)

    def create_item_list(self, parsed_page):
        item_list = {}
        for div in parsed_page:
            local_item = item(div)
            # x = local_item.dict['link'].split('_')
            # item_list[lambda x: len(x) - 1] = local_item.dict
            item_list[local_item.get_id()] = local_item.dict
        return item_list

    def check_item_lists(self, new_list):
        if self.stored_list.keys() != new_list.keys():
            for key in new_list.keys():
                if key not in self.stored_list.keys():
                    self.stored_list = new_list
                    return bot().send_a_message(new_list[key])

class item:
    def __init__(self, div):
        self.dict = {}
        self.div = div
        self.dict['link'] = div.find('a').get('href')
        self.dict['title'] = div.find('a').get_text()
        self.dict['price'] = div.find('div').get_text()
        self.dict['description'] = div.find_all('p')
        # return self.dict

    def get_id(self):
        get_last = lambda x: x[len(x) - 1]
        return get_last(self.dict['link'].split('_'))
        # x = self.dict['link'].split('_')
        # print (x)
        # return lambda x:[len(x) - 1]

class bot:
    def __init__(self):
        self.api_url = 'https://api.telegram.org/bot%s/' % config.token
        self.chat_id = 94925736

    def send_a_message(self, message):
        r = requests.post(self.api_url + 'sendMessage', data={'text': 'https://www.avito.ru' + message['link'], 'chat_id': self.chat_id})
        print ('message: ', message, 'response: ', r.text)

def main():
    global url
    global query
    if len(sys.argv) >= 3:
        section = sys.argv[1]
        query = sys.argv[2]
        url = 'https://www.avito.ru/sankt-peterburg/%s?q=%s' % (section, query)

def test_lists():
    db.stored_list.popitem()
    db.check_item_lists(db.create_item_list(parser(url).page))

if __name__ == '__main__':
    main()
    db = db(parser(url).page)
    db.check_item_lists(db.create_item_list(parser(url).page))   

# example: https://habrahabr.ru/post/302688/