from persiantools.jdatetime import JalaliDateTime

from tasnim_news_crawler import TasnimNewsCrawler


def main():
    start_date = JalaliDateTime.strptime("1403/05/23", '%Y/%m/%d').jalali_date()
    # start_date = JalaliDateTime.today().jalali_date()
    end_date = JalaliDateTime.today().jalali_date()

    news_crawlers = [TasnimNewsCrawler()]
    crawled_news = [news for crawler in news_crawlers for news in crawler.scrape_all_pages(start_date, end_date)]

    print("Crawled News:")
    for date, title in crawled_news:
        print(f"{date}: {title}")


if __name__ == "__main__":
    main()
