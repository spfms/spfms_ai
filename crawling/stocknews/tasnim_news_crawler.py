import requests
from bs4 import BeautifulSoup
from persiantools.jdatetime import JalaliDateTime, JalaliDate

from crawling.stocknews.news_crawler import NewsCrawler


class TasnimNewsCrawler(NewsCrawler):
    def __init__(self):
        base_url = "https://www.tasnimnews.com/fa/service/84/بازار-سهام-سورس?page="
        super().__init__(base_url)

    @staticmethod
    def replace_arabic_characters(text):
        text = text.replace('ي', 'ی')
        text = text.replace('ك', 'ک')
        return text

    def convert_date(self, date_str):
        date_str = self.replace_arabic_characters(date_str)
        if "پیش" in date_str:
            return JalaliDate.today().strftime('%Y/%m/%d')

        try:
            date_part, _ = date_str.split(' - ')
            jalali_date = JalaliDateTime.strptime(date_part, '%d %B %Y', 'fa').jalali_date()
            return jalali_date.strftime('%Y/%m/%d')
        except ValueError:
            return date_str

    def is_within_date_range(self, date_str, start_date, end_date):
        date_obj = JalaliDateTime.strptime(date_str, '%Y/%m/%d').jalali_date()
        return start_date <= date_obj <= end_date

    def scrape_page(self, page_number):
        url = self.base_url + str(page_number)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        news_items = []
        news_section = soup.find('section', class_='content')
        if news_section:
            for article in news_section.find_all('article', class_='list-item'):
                time_tag = article.find('time')
                date = time_tag.text.strip() if time_tag else 'N/A'
                date = self.convert_date(date)

                title_tag = article.find('h2', class_='title')
                title = title_tag.text.strip() if title_tag else 'N/A'

                news_items.append((date, title))

        return news_items
