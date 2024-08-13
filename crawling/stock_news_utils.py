import requests
from bs4 import BeautifulSoup
from persiantools.jdatetime import JalaliDateTime, JalaliDate


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


def is_today(date_str):
    return date_str == JalaliDate.today().strftime('%Y/%m/%d')


def scrape_page(base_url, page_number, is_today_check=False):
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

            if is_today_check and not is_today(date):
                return news_items, False

            title_tag = article.find('h2', class_='title')
            title = title_tag.text.strip() if title_tag else 'N/A'

            news_items.append((date, title))

    return news_items, True if is_today_check else news_items
