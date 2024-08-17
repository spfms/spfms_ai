from persiantools.jdatetime import JalaliDateTime

from crawling.stocknews.tasnim_news_crawler import TasnimNewsCrawler


def scrape_stock_news(start_date=None, end_date=None):
    if not start_date:
        # start_date = JalaliDateTime.strptime("1403/05/26", '%Y/%m/%d').jalali_date()
        start_date = JalaliDateTime.today().jalali_date()
    if not end_date:
        end_date = JalaliDateTime.today().jalali_date()

    news_crawlers = [TasnimNewsCrawler()]
    crawled_news = [news for crawler in news_crawlers for news in crawler.scrape_all_pages(start_date, end_date)]

    return crawled_news


def main():
    return scrape_stock_news()


if __name__ == "__main__":
    print("Crawled News:")
    for date, title in scrape_stock_news():
        print(f"{date}: {title}")
