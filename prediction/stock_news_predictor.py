import joblib

from crawling.today_stock_news_crawl import scrape_today_news


def load_model(model_path):
    """Load the trained model and CountVectorizer."""
    with open(model_path, 'rb') as f:
        model, vectorizer = joblib.load(f)
    return model, vectorizer


def predict_today_news(model, vectorizer, news_list):
    """Predict the label and probability for today's news."""
    news_combined = ' '.join(news_list)
    news_vectorized = vectorizer.transform([news_combined])
    prediction = model.predict(news_vectorized)
    probability = model.predict_proba(news_vectorized)
    return prediction[0], probability[0]


def main(model_path):
    """Main function to get today's news and make predictions."""
    today_news = scrape_today_news()

    if not today_news:
        print("No news found for today.")
        return

    model, vectorizer = load_model(model_path)

    label, probability = predict_today_news(model, vectorizer, today_news)

    print(f"Predicted Label: {label}")
    print(f"Predicted Probability: {probability}")


if __name__ == "__main__":
    model_path = '../models/stock_market_prediction_xgboost_model.pkl'
    main(model_path)
