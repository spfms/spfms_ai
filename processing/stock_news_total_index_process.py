import pandas as pd

# Reading the CSV files
news_df = pd.read_csv('../datasets/stocknews/stock_news.csv', parse_dates=['Date'], encoding='utf-8')
index_df = pd.read_csv('../datasets/indexes/total_index.csv', parse_dates=['Date'], encoding='utf-8')

# Create the 'Label' column (1 if Value > previous day's Value, else 0) and cast to int
index_df['Label'] = (index_df['Value'].diff() > 0).astype(int)

# Group news by date and join news entries
news_grouped = news_df.groupby('Date').agg({'News': ' '.join}).reset_index()

# Merge the two DataFrames on the 'Date' column
merged_df = pd.merge(news_grouped, index_df[['Date', 'Label']], on='Date', how='inner')

# Fill missing 'Label' values by using the next available label value
# merged_df['Label'] = merged_df['Label'].fillna(method='bfill')

# Ensure the 'Label' column is of integer type
merged_df['Label'] = merged_df['Label'].astype(int)

# Saving the merged DataFrame to a new CSV file
output_path = '../datasets/processed/stock_news_total_index_combined.csv'
merged_df.to_csv(output_path, index=False, encoding='utf-8')

print(f"Merged data has been saved to '{output_path}'.")
