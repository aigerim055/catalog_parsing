import csv
from bs4 import ResultSet
import requests
from bs4 import BeautifulSoup
import xlsxwriter 
from decouple import config
import asyncio
import aiohttp
import time



sesssion = requests.Session()
params = {
    'login': 'yes',
}
data = {
    'backurl': '/',
    'AUTH_FORM': 'Y',
    'TYPE': 'AUTH', 
    'USER_LOGIN': config('LOGIN'),
    'USER_PASSWORD': config('PASSWORD'),
}
start_time = time.time()
result = []

async def get_page_data(session, page):
    url = f'https://diler.mosplitka.ru/catalog/?PAGEN_1={page}?login=yes'
    # response = await session.post(url=url, data=data )
    # response_text = await response.text()
    # print(response_text)
    try:
        async with session.get(url=url) as response:
            # print(response)
            response_text = await response.text()
            # print(response_text)

            soup = BeautifulSoup(response_text, "lxml")
            # print(soup)
            
            cards = soup.find_all('div', class_='catalog__result-item')
            

            
            for card in cards: 
                # print(card)
                    
                try:
                    articul = card.find_all('div', class_='catalog__vendor-code')
                except AttributeError:
                    articul = ''

                try:
                    title = card.find('div', class_='catalog__item-descript').find_all('div', class_='catalog__item-name')
                except AttributeError:
                    title = ''
                
                try:
                    country = card.find('div', class_='catalog__item-descript').find('div', class_="catalog__descript-container").find('div', class_='catalog__characteristics').find_all('div', class_="catalog__item-country")
                except AttributeError:
                    country = ''

                try:
                    brand = card.find('div', class_='catalog__item-descript').find('div', class_="catalog__descript-container").find('div', class_='catalog__characteristics').find_all('div', class_="catalog__item-brand")
                except AttributeError:
                    brand = ''

                try:
                    collection = card.find('div', class_='catalog__item-descript').find('div', class_="catalog__descript-container").find('div', class_='catalog__characteristics').find_all('div', class_="catalog__item-collection")
                except AttributeError:
                    collection = ''

                try:
                    color = card.find('div', class_='catalog__item-descript').find('div', class_="catalog__descript-container").find('div', class_='catalog__characteristics').find_all('div', class_="catalog__item-color")
                except AttributeError:
                    color = ''

                try:
                    size = card.find('div', class_='catalog__item-descript').find('div', class_="catalog__descript-container").find('div', class_='catalog__characteristics').find('div', class_="catalog__item-size")
                except AttributeError:
                    size = ''

                try:
                    surface = card.find('div', class_='catalog__item-descript').find('div', class_="catalog__descript-container").find('div', class_='catalog__characteristics').find_all('div', class_="catalog__item-size")
                except AttributeError:
                    surface = ''

                try:
                    packing_size = card.find('div', class_='catalog__packing').find('div', class_="catalog__packing-size").text[:-5]
                except AttributeError:
                    packing_size = ''

                try:
                    packing_size_q = card.find('div', class_='catalog__packing').find('div', class_="catalog__packing-size").text[-5:]
                except AttributeError:
                    packing_size_q = ''

                try:
                    packing_completeness = card.find('div', class_='catalog__packing').find_all('div', class_="catalog__packing-completeness")
                except AttributeError:
                    packing_completeness = ''
                
                try:
                    packing_completeness_q = card.find('div', class_='catalog__packing').find_all('div', class_="catalog__packing-completeness")
                except AttributeError:
                    packing_completeness_q = ''

                try:
                    weight = card.find('div', class_='catalog__pack-weight').text
                except AttributeError:
                    weight = ''

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


                for a in articul:
                    articul = a.text                    

                for a in title:
                    title = a.text

                for a in country:
                    country = a.text[8:]
                
                for a in brand:
                    brand = a.text[15:]

                for a in color:
                    color = a.text[6:]

                for a in collection:
                    collection = a.text[11:]

                for a in size:
                    size = a.text[8:]

                for a in surface:
                    surface = a.text[13:]

                for a in packing_completeness:
                    packing_completeness = a.text.strip(' шт/уп')

                for a in packing_completeness_q:
                    packing_completeness_q = a.text[-5:].strip()

                # for a in weight:
                #     weight = a#.strip(' кг')

                for a in price:
                    price = a.text.strip(' \n ')[:-9]
                    price_q = a.text.strip('\n ')[-9:]

                for a in in_stock_podolsk:
                    in_stock_podolsk = a.text[:-2].strip()
                    in_stock_podolsk_q = a.text[-2:].strip()

                for a in in_stock_krasnodar:
                    in_stock_krasnodar = a.text  

        

                obj = {
                    'articul': articul,
                    'title': title,
                    'country': country,
                    'brand': brand,
                    'collection': collection,
                    'color': color,
                    'size': size,
                    'surface': surface,
                    'packing_size': packing_size,
                    'packing_size_q': packing_size_q,
                    'packing_completeness': packing_completeness,
                    'packing_completeness_q': packing_completeness_q,
                    'weight': weight.strip(' кг\n\t\''),
                    'price': price,
                    'price_q': price_q,
                    'in_stock_podolsk': in_stock_podolsk,
                    'in_stock_podolsk_q': in_stock_podolsk_q,
                    'in_stock_krasnodar': in_stock_krasnodar,
                }

                result.append(obj)
                # print(result)

            OUT_XLSX_FILENAME = 'catalog2.xlsx'
            def write_to_excel(file_name, data):
                """ Запись данных в xlsx файл """
                if not len(data):
                    return None

                with xlsxwriter.Workbook(file_name) as workbook:
                    ws = workbook.add_worksheet()
                    bold = workbook.add_format({'bold': True})
                    headers = ['артикул', 'наименование товара', 'страна', 'производитель', 'коллекция', 'цвет', 'размер','поверхность' , 'упаковка квадратура', 'размерность упаковки', 'пакинг','упаковка кол-во','вес упаковки (кг)', 'цена базовая','размерность цены', 'наличие Подольск','размерность наличия', 'наличие Краснодар']        

                    for col, h in enumerate(headers):
                        ws.write_string(0, col, h, cell_format=bold)

                    for row, item in enumerate(data, start=1):
                        ws.write_string(row, 0, item['articul'])
                        ws.write_string(row, 1, item['title'])
                        ws.write_string(row, 2, item['country'])
                        ws.write_string(row, 3, item['brand'])
                        ws.write_string(row, 4, item['collection'])
                        ws.write_string(row, 5, item['color'])
                        ws.write_string(row, 6, item['size'])
                        ws.write_string(row, 7, item['surface'])
                        ws.write_string(row, 8, item['packing_size'])
                        ws.write_string(row, 9, item['packing_size_q'])
                        ws.write_string(row, 10, item['packing_completeness'])
                        ws.write_string(row, 11, item['packing_completeness_q'])
                        ws.write_string(row, 12, item['weight'])
                        ws.write_string(row, 13, item['price'])
                        ws.write_string(row, 14, item['price_q'])
                        ws.write_string(row, 15, item['in_stock_podolsk'])
                        ws.write_string(row, 16, item['in_stock_podolsk_q'])
                        ws.write_string(row, 17, item['in_stock_krasnodar'])

            write_to_excel(OUT_XLSX_FILENAME, result)

            print(f"[INFO] Обработал страницу {page}")

    except asyncio.TimeoutError:

        print('timeout!')


async def gather_data():

    url = f'https://diler.mosplitka.ru/catalog/?login=yes'

    async with aiohttp.ClientSession() as session:
        proxy_auth = aiohttp.BasicAuth(config('LOGIN'), config('PASSWORD'))
        response = await session.post(url=url)
        soup = BeautifulSoup(await response.text(), "lxml")
        # print(soup)
        pages_count = int(soup.find('div', class_='navigation-pages').find(id="navigation_1_next_page").find_previous_sibling().text)

        tasks = []

        for page in range(1, pages_count):
            # print(page)
            task = asyncio.create_task(get_page_data(session, page))
            tasks.append(task)
            # print(tasks)
            # print(f"[INFO] Обработал страницу {page}")

        await asyncio.gather(*tasks)


def main():
    asyncio.run(gather_data())


    
    
    finish_time = time.time() - start_time
    print(f"Затраченное на работу скрипта время: {finish_time}")


if __name__ == "__main__":
    main()

