import sys, requests
from bs4 import BeautifulSoup

url = ''
query = ''
old_list = {}

def get_items(url):
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    after_ads = soup.find_all('div', {'class': 'js-catalog_after-ads'})
    return after_ads[0].find_all('div', {'class': 'description'})

def get_list():
    global query
    items_dict = {}
    query = query.upper()
    items = get_items(url)
    for item in items:
        title = item.find('a').get_text().upper()
        if title.find(query) != -1:
            items_dict[item.find('a').get('href')] = item
    return items_dict

def check_lists(old):
    global old_list
    new = get_list()
    if old.keys() != new.keys():
        print ('lists are not equal')
    else:
        print ('nothing new')


def send_message(message):
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
    old_list = get_list()

# Q:
# 1. global??
# 2. comparison of two dicts
# 3. method overloading
