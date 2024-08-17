import joblib

from crawling.stocknews.stock_news_crawl import scrape_recent_stock_news


def load_model(model_path):
    """Load the trained model and CountVectorizer."""
    with open(model_path, 'rb') as f:
        model, vectorizer = joblib.load(f)
    return model, vectorizer


def predict_today_news(model, vectorizer, news_list):
    """Predict the label and probability for today's news."""
    news_combined = ' '.join(news_list)
    news_vectorized = vectorizer.transform([news_combined])
    prediction = model.predict(news_vectorized.todense())
    probability = model.predict_proba(news_vectorized.todense())
    return prediction[0], probability[0]


def main(model_path):
    today_news = [(text, source) for _, text, source in scrape_recent_stock_news()]

    if not today_news:
        print("No news found for today.")
        return

    model, vectorizer = load_model(model_path)

    news_by_source = {}
    for text, source in today_news:
        if source not in news_by_source:
            news_by_source[source] = text
        else:
            news_by_source[source] += " " + text

    predictions = {}
    for source, news in news_by_source.items():
        label, prob = predict_today_news(model, vectorizer, [news])
        predictions[source] = {
            "news": news,
            "label": label,
            "probability": prob[label]
        }

    for source, result in predictions.items():
        print(f"Source: {source}")
        print(f"  News: {result['news'][:100]}...")
        print(f"  Predicted Label: {result['label']}")
        print(f"  Predicted Probability: {result['probability']}")
        print()

# Example usage
# main('path_to_your_model')



if __name__ == "__main__":
    model_path = '../models/stock_market_prediction_xgboost_model.pkl'
    main(model_path)
