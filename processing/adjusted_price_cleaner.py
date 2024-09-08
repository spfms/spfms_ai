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

df.to_csv(output_path, index=False)

print("File updated successfully!")
