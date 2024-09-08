import jdatetime
import pandas as pd

from utils.alphabet_util import clean_sentence

file_path = '../datasets/stockprices/Adjusted_Price_report.csv'
output_path = '../datasets/stockprices/Cleaned_Adjusted_Price_report.csv'

df = pd.read_csv(file_path)

df['Ticker'] = df['Ticker'].apply(clean_sentence)


def reformat_date(persian_date):
    jalali_date = jdatetime.date(*map(int, persian_date.split('-')))
    return jalali_date.strftime('%Y/%m/%d')


df['Date'] = df['Date'].apply(reformat_date)

tickers_with_invalid_prices = df[df['Adj Close'].isin([1000, 0])]['Ticker'].unique()

df = df[~df['Ticker'].isin(tickers_with_invalid_prices)]

df.to_csv(output_path, index=False)

print("File updated successfully!")
