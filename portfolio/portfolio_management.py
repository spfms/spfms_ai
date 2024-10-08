import numpy as np
import pandas as pd
from scipy.optimize import minimize


def load_data():
    tickers_df = pd.read_csv('datasets/stockprices/Cleaned_Adjusted_Price_report.csv')
    index_df = pd.read_csv('datasets/indexes/total_index.csv')
    tickers_df.set_index('Date', inplace=True)
    index_df.set_index('Date', inplace=True)
    return tickers_df, index_df


def calculate_returns(tickers_df, index_df, tickers_to_include):
    ticker_prices = tickers_df.pivot(columns='Ticker', values='Adj Close')
    ticker_prices = ticker_prices[tickers_to_include]
    ticker_returns = ticker_prices.pct_change() * 100
    index_returns = index_df['Value'].pct_change() * 100
    return ticker_returns.dropna(), index_returns.dropna()


def calculate_stats(ticker_returns):
    mean_returns = ticker_returns.mean()
    cov_matrix = ticker_returns.cov()
    return mean_returns, cov_matrix


def calculate_weights_from_invested(invested_amounts):
    total_investment = sum(invested_amounts.values())
    weights = {ticker: invested / total_investment for ticker, invested in invested_amounts.items()}
    return weights


def optimize_portfolio(ticker_returns, mean_returns, cov_matrix, initial_weights, risk_free_rate=0):
    tickers = ticker_returns.columns
    num_assets = len(tickers)

    def sharpe_ratio(weights):
        portfolio_return = np.dot(weights, mean_returns)
        portfolio_var = np.dot(weights.T, np.dot(cov_matrix, weights))
        portfolio_stddev = np.sqrt(portfolio_var)
        return -(portfolio_return - risk_free_rate) / portfolio_stddev

    initial_weights_array = np.array([initial_weights.get(ticker, 0) for ticker in tickers])
    constraints = {'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1}
    bounds = tuple((0, 1) for _ in range(num_assets))

    result = minimize(sharpe_ratio, initial_weights_array, method='SLSQP', bounds=bounds, constraints=constraints)

    if not result.success:
        raise ValueError("Optimization failed!")

    return result.x


def calculate_portfolio_performance(weights, ticker_returns, mean_returns, cov_matrix, risk_free_rate=0):
    portfolio_return = np.dot(weights, mean_returns)
    portfolio_var = np.dot(weights.T, np.dot(cov_matrix, weights))
    portfolio_stddev = np.sqrt(portfolio_var)
    sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_stddev
    portfolio_returns = ticker_returns.dot(weights)
    portfolio_cum_returns = (1 + portfolio_returns / 100).cumprod()
    return portfolio_return, portfolio_stddev, sharpe_ratio, portfolio_cum_returns


def calculate_profit_and_loss(portfolio_return, invested_amounts):
    total_investment = sum(invested_amounts.values())
    profit_or_loss = total_investment * (portfolio_return / 100)
    return profit_or_loss


def get_all_tickers():
    tickers_df, _ = load_data()
    all_tickers = tickers_df['Ticker'].unique().tolist()
    return all_tickers


def manage_portfolio(invested_amounts_dict):
    tickers_to_include = list(invested_amounts_dict.keys())

    tickers_df, index_df = load_data()
    ticker_returns, index_returns = calculate_returns(tickers_df, index_df, tickers_to_include)
    mean_returns, cov_matrix = calculate_stats(ticker_returns)

    initial_weights_dict = calculate_weights_from_invested(invested_amounts_dict)

    optimal_weights = optimize_portfolio(ticker_returns, mean_returns, cov_matrix, initial_weights_dict,
                                         risk_free_rate=0)

    initial_weights_array = np.array([initial_weights_dict.get(ticker, 0) for ticker in tickers_to_include])

    initial_return, initial_stddev, initial_sharpe, invested_cum_returns = calculate_portfolio_performance(
        initial_weights_array, ticker_returns, mean_returns, cov_matrix)

    optimized_return, optimized_stddev, optimized_sharpe, optimized_cum_returns = calculate_portfolio_performance(
        optimal_weights, ticker_returns, mean_returns, cov_matrix)

    index_cum_returns = (1 + index_returns / 100).cumprod()

    optimized_portfolio = {ticker: weight * sum(invested_amounts_dict.values())
                           for ticker, weight in zip(tickers_to_include, optimal_weights)}

    comparison_data = {
        'initial_return': initial_return,
        'optimized_return': optimized_return,
        'initial_stddev': initial_stddev,
        'optimized_stddev': optimized_stddev,
        'initial_sharpe': initial_sharpe,
        'optimized_sharpe': optimized_sharpe,
    }

    cum_returns_data = {
        'invested_cum_returns': invested_cum_returns.tolist(),
        'optimized_cum_returns': optimized_cum_returns.tolist(),
        'index_cum_returns': index_cum_returns.tolist()
    }

    risk_vs_return_data = {
        'tickers': ticker_returns.columns.tolist(),
        'returns': mean_returns.tolist(),
        'risks': ticker_returns.std().tolist()
    }

    return {
        'comparison_data': comparison_data,
        'cum_returns_data': cum_returns_data,
        'risk_vs_return_data': risk_vs_return_data,
        'optimized_portfolio': optimized_portfolio
    }
