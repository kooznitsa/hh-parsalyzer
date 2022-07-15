from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import csv
import re
from helpers import *


quote_pages = []

def get_ids(area, metro, filename):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

    if area==cities['Москва']:
        get_urls_cities(1, msk_metro)
    if area==cities['Санкт-Петербург']:
        get_urls_cities(2, spb_metro)
    elif area==areas:
        get_urls_regions(areas)

    data = []

    for pg in quote_pages:
        req = Request(url=pg, headers=headers)
        try:
            page = urlopen(req)
        except:
            continue
        soup = BeautifulSoup(page, 'html.parser')

        listings = soup.findAll('div', class_='vacancy-serp-item')
        for l in listings:
            try:
                href = l.find('a', class_='bloko-button')['href']
                id = href.rsplit('/applicant/vacancy_response?vacancyId=', 1)[1]
                id = re.search(r'\d+', id).group()
            except:
                continue

            data.append((id))
            print(id)

    print('DATA LENGTH:', len(data))

    with open(filename + '.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        for val in data:
            writer.writerow([val])


def get_urls_cities(area, metro):
    for num in range(0,40):
        for m in metro.values():
            url = f'https://spb.hh.ru/search/vacancy?area={area}&metro={m}&search_field=name&search_field=description&text=python&page={num}'
            quote_pages.append(url)
    return quote_pages

def get_urls_regions(areas):
    for num in range(0,40):
        for a in areas:
            url = f'https://spb.hh.ru/search/vacancy?area={a}&search_field=name&search_field=description&text=python&page={num}'
            quote_pages.append(url)
    return quote_pages