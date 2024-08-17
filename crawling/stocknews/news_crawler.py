from abc import ABC, abstractmethod


class NewsCrawler(ABC):
    def __init__(self, base_url):
        self.base_url = base_url

    @abstractmethod
    def scrape_page(self, page_number):
        pass

    @abstractmethod
    def convert_date(self, date_str):
        pass

    @abstractmethod
    def is_within_date_range(self, date_str, start_date, end_date):
        pass

    def scrape_all_pages(self, start_date, end_date):
        all_news = []
        page = 1
        while True:
            news_items = self.scrape_page(page)

            filtered_news = [
                (date, news_text, source) for date, news_text, source in news_items
                if self.is_within_date_range(date, start_date, end_date)
            ]

            if not filtered_news and all_news:
                break

            all_news.extend(filtered_news)
            page += 1

        return all_news
