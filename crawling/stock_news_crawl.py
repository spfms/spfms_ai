import csv
import time

from stock_news_utils import scrape_page

base_url = ("https://www.tasnimnews.com/fa/service/84/%D8%A8%D8%A7%D8%B2%D8%A7%D8%B1-%D8%B3%D9%87%D8%A7%D9%85-%D8%B3"
            "%D9%88%D8%B1%D8%B3?page=")

output_file = '../datasets/stocknews/stock_news.csv'


def scrape_all_pages(start_page, end_page):
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'News'])

        for page in range(start_page, end_page + 1):
            print(f"Scraping page {page}")
            news_items, _ = scrape_page(base_url, page)
            writer.writerows(news_items)
            time.sleep(0.001)


scrape_all_pages(1, 746)
print(f"Scraping completed. Data saved to {output_file}")
