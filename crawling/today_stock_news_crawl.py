import time

from stock_news_crawl import scrape_page

base_url = ("https://www.tasnimnews.com/fa/service/84/%D8%A8%D8%A7%D8%B2%D8%A7%D8%B1-%D8%B3%D9%87%D8%A7%D9%85-%D8%B3"
            "%D9%88%D8%B1%D8%B3?page=")


def scrape_today_news():
    today_news = []
    page = 1
    while True:
        print(f"Scraping page {page}")
        news_items, continue_scraping = scrape_page(base_url, page, is_today_check=True)

        today_news.extend([title for _, title in news_items])

        if not continue_scraping:
            break

        page += 1
        time.sleep(0.001)

    return today_news


if __name__ == "__main__":
    today_news = scrape_today_news()
    print("Today's news:")
    for news in today_news:
        print(news)
