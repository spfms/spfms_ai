import pandas as pd
import numpy as np

# Reading the CSV files
news_df = pd.read_csv('../datasets/stocknews/stock_news.csv', parse_dates=['Date'], encoding='utf-8')
index_df = pd.read_csv('../datasets/indexes/total_index.csv', parse_dates=['Date'], encoding='utf-8')

# Forward fill missing values in the total index DataFrame
index_df['Value'] = index_df['Value'].interpolate(method='linear')

# Group news by date and join news entries
news_grouped = news_df.groupby('Date').agg({'News': ' | '.join}).reset_index()

# Merge the two DataFrames on the 'Date' column
merged_df = pd.merge(news_grouped, index_df, on='Date', how='left')

# Saving the merged DataFrame to a new CSV file
merged_df.to_csv('../datasets/processed/stock_news_total_index_combined.csv', index=False, encoding='utf-8')

print("Merged data has been saved to 'stock_news_total_index_combined.csv'.")
