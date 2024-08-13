import warnings

import joblib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier

warnings.filterwarnings('ignore')

# Load the data
data1 = pd.read_csv('../datasets/processed/stock_news_total_index_combined.csv')

# Split the data into train and test sets
train = data1[data1['Date'] < '1400/12/28']
test = data1[data1['Date'] > '1401/01/01']

# Data cleaning
all_data = [train, test]
for df in all_data:
    df.replace("[^\u0600-\u06FF]", " ", regex=True, inplace=True)

# Prepare headlines
headlines = []
for row in range(0, len(train.index)):
    headlines.append(train.iloc[row, 1])

test_transform = []
for row in range(0, len(test.index)):
    test_transform.append(test.iloc[row, 1])

# Vectorization
countvector = CountVectorizer(ngram_range=(1, 1), max_features=800)
traindataset = countvector.fit_transform(headlines)
test_dataset = countvector.transform(test_transform)

# XGBoost without hyperparameter tuning
xgb = XGBClassifier(random_state=1)
xgb.fit(pd.DataFrame(traindataset.todense(), columns=countvector.get_feature_names_out()), train['Label'])
predictions = xgb.predict(pd.DataFrame(test_dataset.todense(), columns=countvector.get_feature_names_out()))

# Evaluate the XGBoost model
score = accuracy_score(test['Label'], predictions)
print(f"XGBoost Accuracy: {score}")

# Save the XGBoost model
joblib.dump(xgb, '../models/stock_market_prediction_xgboost_model.pkl')
