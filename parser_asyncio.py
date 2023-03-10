import datetime
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import aiohttp
import asyncio
from decouple import config
import time
import csv
import xlsxwriter 
from bs4 import ResultSet



start_time = time.time()
result = []
cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')

ua = UserAgent()
    
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': ua.random
}
data = {
    'backurl': '/',
    'AUTH_FORM': 'Y',
    'TYPE': 'AUTH', 
    'USER_LOGIN': config('LOGIN'),
    'USER_PASSWORD': config('PASSWORD'),
}

async def get_page_data(session,page):
    
    
    url = f'https://diler.mosplitka.ru/catalog'
    response = await session.post(url=url, data=data, headers=headers, timeout=3000)
    soup = BeautifulSoup(await response.text(), "lxml")

    async with aiohttp.ClientSession(trust_env=True, timeout=3000) as session:
        
        try:
            cards: ResultSet = soup.find('div', class_="catalog__inner-container catalog__inner-container--content").find_all('div', class_='catalog__result-item')
        except AttributeError:
            try:
                await asyncio.sleep(60)
                cards: ResultSet = soup.find('div', class_="catalog__inner-container catalog__inner-container--content").find_all('div', class_='catalog__result-item')
            except AttributeError:
                await asyncio.sleep(120)
                cards: ResultSet = soup.find('div', class_="catalog__inner-container catalog__inner-container--content").find_all('div', class_='catalog__result-item')


        for card in cards: 
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
                    packing_completeness = a.text.strip(' ????/????')

                for a in packing_completeness_q:
                    packing_completeness_q = a.text[-5:].strip()

                # for a in weight:
                #     weight = a#.strip(' ????')

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
                    'weight': weight.strip(' ????\n\t\''),
                    'price': price,
                    'price_q': price_q,
                    'in_stock_podolsk': in_stock_podolsk,
                    'in_stock_podolsk_q': in_stock_podolsk_q,
                    'in_stock_krasnodar': in_stock_krasnodar,
                }

                result.append(obj)

        # def write_to_csv(data: list):
        #     """ ???????????? ???????????? ?? csv ???????? """
        #     fieldnames = ['articul',
        #                             'title',
        #                             'country',
        #                             'brand',
        #                             'collection',
        #                             'color',
        #                             'size',
        #                             'surface',
        #                             'packing_size',
        #                             'packing_size_q',
        #                             'packing_completeness',
        #                             'packing_completeness_q',
        #                             'weight',
        #                             'price',
        #                             'price_q',
        #                             'in_stock_podolsk',
        #                             'in_stock_podolsk_q',
        #                             'in_stock_krasnodar']
        #     with open('test.csv', 'w') as file:
        #         csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        #         csv_writer.writeheader()
        #         csv_writer.writerows(data)

        # # print(result)
        # write_to_csv(result)
        print(f"[INFO] ?????????????????? ???????????????? {page}")


OUT_XLSX_FILENAME = f'catalog_{cur_time}.xlsx'
def write_to_excel(file_name, data):
    """ ???????????? ???????????? ?? xlsx ???????? """
    if not len(data):
        return None

    with xlsxwriter.Workbook(file_name) as workbook:
        ws = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True})
        headers = ['??????????????', '???????????????????????? ????????????', '????????????', '??????????????????????????', '??????????????????', '????????', '????????????','??????????????????????' , '???????????????? ????????????????????', '?????????????????????? ????????????????', '????????????','???????????????? ??????-????','?????? ???????????????? (????)', '???????? ??????????????','?????????????????????? ????????', '?????????????? ????????????????','?????????????????????? ??????????????', '?????????????? ??????????????????']        

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


async def gather_data():

    url = f'https://diler.mosplitka.ru/catalog/?login=yes'

    async with aiohttp.ClientSession(trust_env=True) as session:
        response = await session.post(url=url, data=data, headers=headers)
        soup = BeautifulSoup(await response.text(), "lxml")
        # print(soup)
        pages_count = int(soup.find('div', class_='navigation-pages').find(id="navigation_1_next_page").find_previous_sibling().text)

        tasks = []

        for page in range(1,pages_count + 1):
            await asyncio.sleep(1.4)
            task = asyncio.create_task(get_page_data(session, page))
            tasks.append(task)
        await asyncio.gather(*tasks)


def main():
    asyncio.run(gather_data())
    write_to_excel(OUT_XLSX_FILENAME, result)
    finish_time = time.time() - start_time
    print(f"?????????????????????? ???? ???????????? ?????????????? ??????????: {finish_time}")


if __name__ == "__main__":
    main()