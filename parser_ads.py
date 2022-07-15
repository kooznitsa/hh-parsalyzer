from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
import csv
import re
import time


pages = []
data = []


def get_listings(id_list, filename):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

    create_urls(id_list)

    scrape_data(pages, headers)

    columns = ['ID', 'Регион', 'Должность', 'Зарплата от', 'Зарплата до', 'Способ оплаты', \
        'Работодатель', 'Адрес', 'Опыт работы', 'Режим работы', 'Навыки', 'Дата', 'Описание']

    with open(filename + '.csv', 'w', encoding='utf-16') as csv_file:
        writer = csv.writer(csv_file, lineterminator='\n', delimiter ='\t')
        writer.writerow((columns))
        writer.writerows(data)


def create_urls(id_list):
    df = pd.read_csv(id_list, encoding='utf-8', delimiter='\t', index_col=None, header=None)
    df = df.drop_duplicates(keep='first')

    for id in df.values:
        url = f'https://hh.ru/vacancy/{str(id)[1:-1]}'
        pages.append(url)

    return pages


def scrape_data(pages, headers):
    for pg in pages:
        req = Request(url=pg, headers=headers)
        try:
            page = urlopen(req)
        except:
            continue
        soup = BeautifulSoup(page, 'html.parser')

        try:
            container = soup.findAll('div', class_='bloko-columns-row')[0]
        except: 
            continue
        
        try:
            href = container.find('a', class_='bloko-button')['href']
            id = href.rsplit('/applicant/vacancy_response?vacancyId=', 1)[1]
            id = re.search(r'\d+', id).group()
        except:
            continue

        address = getattr(container.find('span', attrs={'data-qa': 'vacancy-view-raw-address'}), 'text', None)

        try:
            location = container.find('p', attrs={'data-qa': 'vacancy-view-location'}).text
        except:
            try:
                location = address.split(',')[0]
            except:
                location = None

        title = getattr(container.find('h1', attrs={'data-qa':'vacancy-title'}), 'text', None)

        salary = getattr(container.find('span', attrs={'data-qa': 'vacancy-salary-compensation-type-net'}), 'text', None)
        try:
            salary_from = salary.rsplit('от', 1)[1]
            salary_from = re.search(r'\d+', salary_from).group()
        except:
            salary_from = None
        try:
            salary_to = salary.rsplit('до', 1)[1]
            salary_to = re.search(r'\d+', salary_to).group()
        except:
            salary_to = None

        try:
            numbers = []
            for word in salary.split():
                if word.isdigit():
                    numbers.append(word)

            stopwords = ['от', 'до', 'руб.']
            stopwords += numbers
            result_words  = [word for word in salary.split() if word.lower() not in stopwords]
            salary_mode = ' '.join(result_words)
        except:
            salary_mode = None

        employer = getattr(container.find('div', attrs={'data-qa': 'vacancy-company__details'}), 'text', None)

        experience = getattr(container.find('span', attrs={'data-qa': 'vacancy-experience'}), 'text', None)

        employment = getattr(container.find('p', attrs={'data-qa': 'vacancy-view-employment-mode'}), 'text', None)
        employment_modes = []
        try:
            for em in employment.split(','):
                employment_modes.append(em)
        except:
            employment_modes = []
        
        try:
            skills = []
            skills_list = container.findAll('span', class_='bloko-tag__section_text')
            for skill in skills_list:
                skills.append(skill.get_text())
        except:
            skills = None
        
        date_string = getattr(container.find('p', class_='vacancy-creation-time-redesigned'), 'text', None)
        try:
            date = date_string.rsplit('Вакансия опубликована ', 1)[1]
            date = date.rsplit('в ', 1)[0]
        except:
            date = None

        description = getattr(container.find('div', attrs={'data-qa': 'vacancy-description'}), 'text', None)

        time.sleep(2)

        data.append((id, location, title, salary_from, salary_to, salary_mode, employer, \
            address, experience, employment_modes, skills, date, description))
        print('DATA APPENDED:', pg)