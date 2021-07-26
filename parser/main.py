import requests
import csv
import time
from bs4 import BeautifulSoup
from selenium import webdriver


URL = 'https://www.ozon.ru/category/smartfony-15502/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/43.4',
    'accept': '*/*'}
FILE = 'mobiles.csv'


def get_data_with_selenium(url):
    options = webdriver.FirefoxOptions()
    options.set_preference("general.useragent.override", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36")

    try:
        driver = webdriver.Firefox(
            executable_path="/Users/karenkocharyan/PycharmProjects/parser/geckodriver",
            options=options
        )
        driver.get(url=url)
        time.sleep(5)

        with open("index_selenium.html", "w") as file:
            file.write(driver.page_source)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

    with open("index_selenium.html") as file:
        src = file.read()

    return src


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['title', 'char', 'price'])
        for item in items:
            writer.writerow([item['title'], item['characteristics'], item['price']])


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(get_data_with_selenium(html), "lxml")
    items = soup.find_all('div', class_='a0c6 a0d')

    mobiles = []
    for item in items:
        if (item.find('span', class_='j4 as3 az a0f2 f-tsBodyL item b3u9 a1d1')) and item.find('span', class_='j4 as3 a0f6 f-tsBodyM item a1d1') and item.find('span', 'b5v6 b5v7 c4v8'):
            mobiles.append({
                'title': item.find('span', class_='j4 as3 az a0f2 f-tsBodyL item b3u9 a1d1').get_text(),
                'characteristics': item.find('span', class_='j4 as3 a0f6 f-tsBodyM item a1d1').get_text().replace(', дюймы',
                                                                                                                  '').replace(
                    ', Мпикс', ''),
                'price': item.find('span', 'b5v6 b5v7 c4v8').get_text().replace('\u202f', '').replace('₽', '')
            })
        elif (item.find('span', class_='j4 as3 az a0f2 f-tsBodyL item b3u9 a1d1')) and item.find('span', class_='j4 as3 a0f6 f-tsBodyM item a1d1') and item.find('span', 'b5v6 b5v7'):
            mobiles.append({
                'title': item.find('span', class_='j4 as3 az a0f2 f-tsBodyL item b3u9 a1d1').get_text(),
                'characteristics': item.find('span', class_='j4 as3 a0f6 f-tsBodyM item a1d1').get_text().replace(', дюймы',
                                                                                                                  '').replace(
                    ', Мпикс', ''),
                'price': item.find('span', 'b5v6 b5v7').get_text().replace('\u202f', '').replace('₽', '')
            })
    return mobiles


def parse():
    html = get_html(URL)
    mobiles = []
    if html.status_code == 200:
        for page in range(1, 177):
            print(f'Парсинг страницы {page} из {177}...')
            try:
                html = get_html(URL, params={'page': page})
                print(html.url)
                mobiles.extend(get_content(html.url))
            except Exception as ex:
                print(ex)
        save_file(mobiles, FILE)
        print(f'Получено {len(mobiles)} смартфонов')
    else:
        print('Error')


def main():
    parse()


if __name__ == '__main__':
    main()



