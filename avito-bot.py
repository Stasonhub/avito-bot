import sys, requests
from bs4 import BeautifulSoup

html = ''
query = ''

list_data = list()

def get_items(html):
    soup = BeautifulSoup(html, 'html.parser')
    after_ads = soup.find_all('div', {'class': 'js-catalog_after-ads'})
    return after_ads[0].find_all('div', {'class': 'description'})

def create_dict(items):
    items_dict = {}
    for item in items:
        title = item.find('a').get_text().capitalize()
        if title.find(query.capitalize()):
            items_dict[item.find('a').get('href')] = item
    return items_dict

def main():
    global html
    global query
    if len(sys.argv) >= 3:
        section = sys.argv[1]
        query = sys.argv[2]
        url = 'https://www.avito.ru/sankt-peterburg/%s?q=%s' % (section, query)
        html = requests.get(url).text

if __name__ == '__main__':
    main()
    items = get_items(html)
    d = create_dict(items)
    print (d)
    # items = BeautifulSoup(str(items), 'html.parser')

# >>> items[0].find('a').get('href')
# '/sankt-peterburg/telefony/meizu_mx5_761685191'
# >>> items[0].find('a').get_text()


# >>> for item in items:
# ...     text = item.find('a').get_text()
# ...     text.capitalize()
# ...     text = text.capitalize()
# ...     if text.find(q.capitalize()):
# ...             print (item)
