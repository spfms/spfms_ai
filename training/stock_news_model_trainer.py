import re
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import hazm  # Persian NLP library

# Load the data
data1 = pd.read_csv('../datasets/processed/stock_news_total_index_combined.csv')

# Split the data into train and test sets
train = data1[data1['Date'] < '1400/12/28']
test = data1[data1['Date'] > '1401/01/01']

# Initialize Hazm tools for Persian NLP
normalizer = hazm.Normalizer()
lemmatizer = hazm.Lemmatizer()
stop_words = hazm.stopwords_list()

def clean_text(text):
    # Normalize the text
    text = normalizer.normalize(text)
    # Remove non-Persian characters and extra spaces
    text = re.sub("[^\u0600-\u06FF\s]", " ", text)
    text = re.sub("\s+", " ", text)
    # Tokenize the text
    tokens = hazm.word_tokenize(text)
    # Remove stopwords and perform lemmatization
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
    return " ".join(tokens)

# Apply cleaning to train and test datasets
train['Cleaned_News'] = train['News'].apply(clean_text)
test['Cleaned_News'] = test['News'].apply(clean_text)

# Prepare headlines
headlines = train['Cleaned_News'].tolist()
test_transform = test['Cleaned_News'].tolist()

# Vectorization using TF-IDF
tfidfvector = TfidfVectorizer(ngram_range=(1, 2), max_features=800)
traindataset = tfidfvector.fit_transform(headlines)
test_dataset = tfidfvector.transform(test_transform)

# Optionally, apply PCA to reduce dimensionality
pca = PCA(n_components=100)
train_pca = pca.fit_transform(traindataset.todense())
test_pca = pca.transform(test_dataset.todense())

# XGBoost without hyperparameter tuning
xgb = XGBClassifier(random_state=1)
xgb.fit(train_pca, train['Label'])
predictions = xgb.predict(test_pca)

# Evaluate the XGBoost model
score = accuracy_score(test['Label'], predictions)
print(f"XGBoost Accuracy: {score}")

# Save the XGBoost model
joblib.dump(xgb, '../models/stock_market_prediction_xgboost_model.pkl')
