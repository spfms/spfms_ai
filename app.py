import json
import os

from flask import Flask, jsonify, request
from flask_cors import CORS

from portfolio.portfolio_management import manage_portfolio, get_all_tickers

app = Flask(__name__)

CORS(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/stock-market-predictions', methods=['GET'])
def get_predictions():
    json_path = os.path.join('datasets', 'predictions', 'stock_market_predictions.json')

    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON"}), 500

    return jsonify(data), 200, {'Content-Type': 'application/json; charset=utf-8'}


@app.route('/tickers', methods=['GET'])
def get_stock_tickers():
    try:
        tickers = get_all_tickers()
        return jsonify({'stock-tickers': tickers}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/manage-stock-portfolio', methods=['POST'])
def manage_stock_portfolio():
    try:
        invested_amounts_dict = request.json.get('invested_amounts_dict')

        if not invested_amounts_dict:
            return jsonify({'error': 'Invalid input: invested_amounts_dict is required'}), 400

        portfolio_data = manage_portfolio(invested_amounts_dict)

        return jsonify(portfolio_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
