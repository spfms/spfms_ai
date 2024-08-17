import json

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


def main(model_path, output_json_path):
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

    predictions = []
    for source, news in news_by_source.items():
        label, prob = predict_today_news(model, vectorizer, [news])
        predictions.append({
            "trend": 'bullish' if label == 1 else 'bearish',
            "confidence": str(prob[label]),
            "source": source
        })

    with open(output_json_path, 'w', encoding='utf-8') as outfile:
        json.dump({"forecasts": predictions}, outfile, ensure_ascii=False, indent=4)

    print(f"Predictions saved to {output_json_path}")


if __name__ == "__main__":
    model_path = '../models/stock_market_prediction_xgboost_model.pkl'
    output_json_path = '../datasets/predictions/stock_market_predictions.json'
    main(model_path, output_json_path)
