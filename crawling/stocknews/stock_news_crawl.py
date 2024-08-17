from persiantools.jdatetime import JalaliDateTime
from datetime import timedelta
from crawling.stocknews.shahre_khabar_news_crawler import ShahreKhabarNewsCrawler


def scrape_recent_stock_news():
    start_date = JalaliDateTime.today().jalali_date() - timedelta(days=1)
    end_date = JalaliDateTime.today().jalali_date()

    news_crawlers = [ShahreKhabarNewsCrawler()]
    crawled_news = [news for crawler in news_crawlers for news in crawler.scrape_all_pages(start_date, end_date)]

    return crawled_news


def main():
    return scrape_recent_stock_news()


if __name__ == "__main__":
    print("Crawled News:")
    for date, news_text, source in scrape_recent_stock_news():
        print(f"{date}: {news_text} / {source}")
