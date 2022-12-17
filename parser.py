import csv
from bs4 import ResultSet
import requests
from bs4 import BeautifulSoup
from decouple import config


session = requests.Session()
url = 'https://diler.mosplitka.ru/'

params = {
    'login': 'yes',
}

data = {
    'backurl': '/',
    'AUTH_FORM': 'Y',
    'TYPE': 'AUTH',
    'USER_LOGIN': '553801042839',
    'USER_PASSWORD': 'u9aADH35BKtN2CK',
    # 'USER_LOGIN': config('LOGIN'),
    # 'USER_PASSWORD': config('PASSWORD'),
}

response = requests.post('https://diler.mosplitka.ru/', params=params, data=data)
# print(response.text)

class Parser:

    def get_html():
        """ Функция для получения html кода """
        url = 'https://diler.mosplitka.ru/catalog/?login=yes'
        response = session.post(url=url, params=params, data=data)
        html = response.text
        # print(html)
        return html


    def get_card_from_html(html: str) -> ResultSet:
        """ Функция для получения карточек из html-кода """
        soup = BeautifulSoup(html, 'lxml')
        cards: ResultSet = soup.find_all('div', class_='catalog__result-item')
        return cards

    def parse_data_from_cards(cards: ResultSet) -> list:
        """ Фильтрация данных из карточек """
        result = []
        for card in cards:
            
                
            try:
                articul = card.find_all('div', class_='catalog__vendor-code')
            except AttributeError:
                articul = ''

            try:
                title = card.find('div', class_='catalog__item-descript').find('div', class_="catalog__descript-container").find_all('div', class_='catalog__item-name')
            except AttributeError:
                title = ''
            
            try:
                desc1 = card.find('div', class_='catalog__item-descript').find('div', class_="catalog__descript-container").find('div', class_='catalog__characteristics').find_all('div', class_="catalog__item-country")
            except AttributeError:
                desc1 = ''

            try:
                desc2 = card.find('div', class_='catalog__item-descript').find('div', class_="catalog__descript-container").find('div', class_='catalog__characteristics').find_all('div', class_="catalog__item-brand")
            except AttributeError:
                desc2 = ''

            try:
                desc3 = card.find('div', class_='catalog__item-descript').find('div', class_="catalog__descript-container").find('div', class_='catalog__characteristics').find_all('div', class_="catalog__item-collection")
            except AttributeError:
                desc3 = ''

            try:
                desc4 = card.find('div', class_='catalog__item-descript').find('div', class_="catalog__descript-container").find('div', class_='catalog__characteristics').find_all('div', class_="catalog__item-color")
            except AttributeError:
                desc4 = ''

            try:
                desc5 = card.find('div', class_='catalog__item-descript').find('div', class_="catalog__descript-container").find('div', class_='catalog__characteristics').find_all('div', class_="catalog__item-size")
            except AttributeError:
                desc5 = ''

            try:
                desc6 = card.find('div', class_='catalog__packing').find_all('div', class_="catalog__packing-size")
            except AttributeError:
                desc6 = ''

            try:
                desc7 = card.find('div', class_='catalog__packing').find_all('div', class_="catalog__packing-completeness")
            except AttributeError:
                desc7 = ''
            
            try:
                desc8 = card.find_all('div', class_='catalog__pack-weight')
            except AttributeError:
                desc8 = ''

            try:
                price = card.find_all('div', class_='catalog__basic-price')
            except AttributeError:
                price = ''

            try:
                in_stock_podolsk = card.find_all('div', class_="catalog__existence")[0] #FIX
            except AttributeError:
                in_stock_podolsk = ''

            try:
                in_stock_krasnodar = card.find_all('div', class_="catalog__existence catalog__existence--krasnodar") 
            except AttributeError:
                in_stock_krasnodar = ''

            description = desc1+ desc2 + desc3 + desc4 + desc5 
            description_packing = desc6 + desc7 + desc8

            for a in articul:
                articul = a.text

            for a in title:
                title = a.text

            for a in desc1:
                desc1 = a.text + ' '
            
            for a in desc2:
                desc2 = a.text + ' '

            for a in desc3:
                desc3 = a.text + ' '

            for a in desc4:
                desc4 = a.text + ' '

            for a in desc5:
                desc5 = a.text + ' '

            for a in desc6:
                desc6 = a.text + ' '
                # print(desc6)

            for a in desc7:
                desc7 = a.text.strip() + ' '
                # print(desc7)

            for a in desc8:
                desc8 = a.text.strip() + ' '
                # print(desc8)

            for a in price:
                price = a.text.strip()

            for a in in_stock_podolsk:
                in_stock_podolsk = a.text
                # print(in_stock_podolsk)

            for a in in_stock_krasnodar:
                in_stock_krasnodar = a.text  

            description = desc1+ desc2 + desc3 + desc4 + desc5 
            description_packing = f'{desc6} {desc7} {desc8}'

            obj = {
               'articul': articul,
               'title': title,
               'description': description,
               'description_packing': description_packing,
               'price': price,
               'in_stock_podolsk': in_stock_podolsk,
               'in_stock_krasnodar': in_stock_krasnodar,
            }

            result.append(obj)
        return result


    def pages(self):
        pages = '?PAGEN_1='
        html = self.get_html()
        pages: ResultSet = html.find('div', class_='navigarion-catalog')#.find('div', class_='navigation-pages').find_all('a')
        # print(pages)

    def get_last_page(html):
        """ Получение количества страниц """
        soup = BeautifulSoup(html, 'lxml')
        # print(soup)
        total_pages = soup.find('div', class_='navigation-catalog').find('div', class_='navigation-pages').find_all('a')[-2]
        # a = total_pages.find('div', class_='navigation-catalog')
        # print(total_pages)
        # pages = soup.find('div', class_='navigation-catalog').find('div', class_='navigation-pages')
        # last_page = pages.find_all('span', class_='nav-current-page')[1]
        # print(last_page)
        # return int(last_page)
        last_page = total_pages.text
        return int(last_page)
    
    def write_to_csv(data: list):
        """ Запись данных в csv файл """
        fieldnames = ['articul', 'title', 'description', 'description_packing', 'price', 'in_stock_podolsk', 'in_stock_krasnodar']
        with open('test.csv', 'w') as file:
            csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
            csv_writer.writeheader()
            csv_writer.writerows(data)
    
    html = get_html()
    # print(get_last_page(html))
    # items = self.soup(html).find('div', class_='navigarion-catalog').find('div', class_='navigation-pages').find_all('a')

    # html = get_html()
    # cards = get_card_from_html(html=html)
    # print(parse_data_from_cards(cards=cards))
    # print(get_last_page())

    result = []
    for page in range(1, get_last_page(html)):
        cards = get_card_from_html(html=html)
        list_of_cards = parse_data_from_cards(cards=cards)
        print(list_of_cards)
        result.extend(list_of_cards)
        # write_to_csv(result)
        # print(result)


if __name__ == '__main__':
    obj = Parser()
    print(obj)
    # obj
