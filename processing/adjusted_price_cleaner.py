import jdatetime
import pandas as pd

from utils.alphabet_util import clean_sentence

file_path = '../datasets/stockprices/Adjusted_Price_report.csv'
output_path = '../datasets/stockprices/Cleaned_Adjusted_Price_report.csv'

# Read the CSV file
df = pd.read_csv(file_path)

# Apply cleaning to 'Ticker' column
df['Ticker'] = df['Ticker'].apply(clean_sentence)


# Define the function to reformat Persian dates to Gregorian dates
def reformat_date(persian_date):
    jalali_date = jdatetime.date(*map(int, persian_date.split('-')))
    return jalali_date.strftime('%Y/%m/%d')


# Apply date reformatting
df['Date'] = df['Date'].apply(reformat_date)

tickers_to_remove = ['وکغدیر1', 'اردستان1', 'کیمیا1', 'ومهان1']
df = df[~df['Ticker'].isin(tickers_to_remove)]

# Save the cleaned DataFrame to a new CSV file
df.to_csv(output_path, index=False)

print("File updated successfully!")
