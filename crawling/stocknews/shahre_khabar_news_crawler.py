from datetime import timedelta

import requests
from bs4 import BeautifulSoup
from persiantools.jdatetime import JalaliDateTime, JalaliDate

from crawling.stocknews.news_crawler import NewsCrawler
from utils.alphabet_util import clean_sentence


class ShahreKhabarNewsCrawler(NewsCrawler):
    def __init__(self):
        base_url = "https://www.shahrekhabar.com/tag/%D8%A8%D9%88%D8%B1%D8%B3?page="
        super().__init__(base_url)

    def convert_date(self, date_str):
        date_str = clean_sentence(date_str)

        if any(unit in date_str for unit in ["ثانیه پیش", "دقیقه پیش", "ساعت پیش"]):
            return JalaliDate.today().strftime('%Y/%m/%d')

        if "روز پیش" in date_str:
            days_ago = int(date_str.split()[0])
            target_date = JalaliDate.today() - timedelta(days=days_ago)
            return target_date.strftime('%Y/%m/%d')

        return date_str

    def is_within_date_range(self, date_str, start_date, end_date):
        try:
            date_obj = JalaliDateTime.strptime(date_str, '%Y/%m/%d').jalali_date()
            return start_date <= date_obj <= end_date
        except ValueError:
            return False

    def scrape_page(self, page_number):
        url = self.base_url + str(page_number)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        news_items = []
        news_list = soup.find('ul', class_='news-list-items clearfix')

        if news_list:
            articles = news_list.find_all('li')

            for article in articles:
                title_tag = article.find('a', class_='alink nlinkb1')
                news_text = clean_sentence(title_tag.text.strip()) if title_tag else 'N/A'

                source_tag = article.find('span', class_='refrence3align')
                source = source_tag.text.strip() if source_tag else 'N/A'

                date_tag = source_tag.find_next_sibling('span', class_='refrence')
                date = date_tag.text.strip() if date_tag else 'N/A'
                date = self.convert_date(date)

                news_items.append((date, news_text, source))

        return news_items
