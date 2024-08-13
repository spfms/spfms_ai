import re

import hazm
import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier

output_path = '../models/stock_market_prediction_xgboost_model.pkl'

dataset = pd.read_csv('../datasets/processed/stock_news_total_index_combined.csv')

training_data = dataset[dataset['Date'] < '1400/12/28'].copy()
testing_data = dataset[dataset['Date'] > '1401/01/01'].copy()


def preprocess_text(text):
    text = re.sub(
        r"[^\u0622\u0627\u0628\u067E\u062A-"
        r"\u062C\u0686\u062D-"
        r"\u0632\u0698\u0633-"
        r"\u063A\u0641\u0642\u06A9\u06AF\u0644-"
        r"\u0648\u06CC]+",
        " ", text)
    tokens = hazm.word_tokenize(text)
    return " ".join(tokens)


training_data['Processed_News'] = training_data['News'].apply(preprocess_text)
testing_data['Processed_News'] = testing_data['News'].apply(preprocess_text)

training_texts = training_data['Processed_News'].tolist()
testing_texts = testing_data['Processed_News'].tolist()

count_vectorizer = CountVectorizer(ngram_range=(1, 2), max_features=800)
X_train = count_vectorizer.fit_transform(training_texts)
X_test = count_vectorizer.transform(testing_texts)

xgb_model = XGBClassifier(random_state=1)
xgb_model.fit(np.asarray(X_train.todense()), training_data['Label'])

predictions = xgb_model.predict(np.asarray(X_test.todense()))
accuracy = accuracy_score(testing_data['Label'], predictions)
print(f"XGBoost Model Accuracy: {accuracy:.4f}")

# Save both the model and the vectorizer
joblib.dump((xgb_model, count_vectorizer), output_path)
print(f'Model and vectorizer saved to {output_path}')
