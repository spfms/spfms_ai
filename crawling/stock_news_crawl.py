import csv
import time

import requests
from bs4 import BeautifulSoup
from persiantools.jdatetime import JalaliDateTime, JalaliDate

base_url = ("https://www.tasnimnews.com/fa/service/84/%D8%A8%D8%A7%D8%B2%D8%A7%D8%B1-%D8%B3%D9%87%D8%A7%D9%85-%D8%B3"
            "%D9%88%D8%B1%D8%B3?page=")

output_file = '../datasets/stocknews/stock_news.csv'


def replace_arabic_characters(text):
    text = text.replace('ي', 'ی')
    text = text.replace('ك', 'ک')

    return text


def convert_date(date_str):
    date_str = replace_arabic_characters(date_str)

    if "پیش" in date_str:
        return JalaliDate.today().strftime('%Y/%m/%d')

    try:
        date_part, time_part = date_str.split(' - ')
        jalali_date = JalaliDateTime.strptime(date_part, '%d %B %Y', 'fa').jalali_date()
        return jalali_date.strftime('%Y/%m/%d')
    except ValueError:
        return date_str


def scrape_page(page_number):
    url = base_url + str(page_number)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    news_items = []

    news_section = soup.find('section', class_='content')
    if news_section:
        for article in news_section.find_all('article', class_='list-item'):
            time_tag = article.find('time')
            date = time_tag.text.strip() if time_tag else 'N/A'
            date = convert_date(date)

            title_tag = article.find('h2', class_='title')
            title = title_tag.text.strip() if title_tag else 'N/A'

            news_items.append((date, title))

    return news_items


def scrape_all_pages(start_page, end_page):
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'News'])

        for page in range(start_page, end_page + 1):
            print(f"Scraping page {page}")
            news_items = scrape_page(page)
            writer.writerows(news_items)

            time.sleep(0.001)


scrape_all_pages(1, 746)

print(f"Scraping completed. Data saved to {output_file}")
