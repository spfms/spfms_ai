import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
from scipy.linalg import cholesky
from scipy.optimize import minimize


def load_data():
    tickers_df = pd.read_csv('../datasets/stockprices/Cleaned_Adjusted_Price_report.csv')
    index_df = pd.read_csv('../datasets/indexes/total_index.csv')
    tickers_df.set_index('Date', inplace=True)
    index_df.set_index('Date', inplace=True)
    return tickers_df, index_df


def calculate_returns(tickers_df, index_df):
    ticker_prices = tickers_df.pivot(columns='Ticker', values='Adj Close')
    ticker_returns = ticker_prices.pct_change() * 100
    index_returns = index_df['Value'].pct_change() * 100
    return ticker_returns.dropna(), index_returns.dropna()


def calculate_stats(ticker_returns):
    mean_returns = ticker_returns.mean()
    variances = ticker_returns.var()
    cov_matrix = ticker_returns.cov()

    try:
        cholesky(cov_matrix)
    except np.linalg.LinAlgError:
        cov_matrix = make_positive_definite(cov_matrix)

    return mean_returns, variances, cov_matrix


def make_positive_definite(cov_matrix):
    eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
    eigenvalues = np.where(eigenvalues < 0, 0, eigenvalues)
    return np.dot(eigenvectors, np.dot(np.diag(eigenvalues), eigenvectors.T))


def optimize_portfolio(ticker_returns, cov_matrix):
    tickers = ticker_returns.columns
    num_assets = len(tickers)
    weights = np.ones(num_assets) / num_assets

    def portfolio_variance(weights, cov_matrix):
        return np.dot(weights.T, np.dot(cov_matrix, weights))

    constraints = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1})
    bounds = tuple((0, 1) for _ in range(num_assets))
    result = minimize(portfolio_variance, weights, args=(cov_matrix,), method='SLSQP', bounds=bounds,
                      constraints=constraints)

    if not result.success:
        raise ValueError("Optimization failed!")

    return result.x


def calculate_portfolio_performance(weights, ticker_returns, mean_returns, cov_matrix):
    portfolio_return = np.dot(weights, mean_returns)
    portfolio_var = np.dot(weights.T, np.dot(cov_matrix, weights))
    portfolio_stddev = np.sqrt(portfolio_var)
    risk_free_rate = 0
    sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_stddev
    portfolio_returns = ticker_returns.dot(weights)
    portfolio_cum_returns = (1 + portfolio_returns / 100).cumprod()
    return portfolio_return, portfolio_stddev, sharpe_ratio, portfolio_cum_returns


def plot_cumulative_returns(portfolio_cum_returns, index_returns):
    index_cum_returns = (1 + index_returns / 100).cumprod()
    plt.figure(figsize=(10, 6))
    plt.plot(portfolio_cum_returns.index, portfolio_cum_returns, label='Portfolio Cumulative Return', color='blue')
    plt.plot(index_cum_returns.index, index_cum_returns, label='Index Cumulative Return', color='red')
    plt.title('Cumulative Returns: Portfolio vs Index')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Return (%)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_risk_return_comparison(ticker_returns, mean_returns):
    risk = ticker_returns.std()
    returns = mean_returns
    fig_data = pd.DataFrame({'Ticker': ticker_returns.columns, 'Return': returns.values, 'Risk': risk.values})
    fig = px.scatter(fig_data, x='Risk', y='Return', text='Ticker', title='Risk vs Return Comparison (Tickers)',
                     labels={'Risk': 'Annualized Risk (%)', 'Return': 'Annualized Return (%)'}, template="plotly_dark")
    fig.show()


tickers_df, index_df = load_data()
ticker_returns, index_returns = calculate_returns(tickers_df, index_df)
mean_returns, variances, cov_matrix = calculate_stats(ticker_returns)
optimal_weights = optimize_portfolio(ticker_returns, cov_matrix)
portfolio_return, portfolio_stddev, sharpe_ratio, portfolio_cum_returns = calculate_portfolio_performance(
    optimal_weights, ticker_returns, mean_returns, cov_matrix)
plot_cumulative_returns(portfolio_cum_returns, index_returns)
plot_risk_return_comparison(ticker_returns, mean_returns)
print("Optimal Weights:", optimal_weights)
print(f"Expected Portfolio Return: {portfolio_return:.2f}%")
print(f"Portfolio Risk (Std Dev): {portfolio_stddev:.2f}%")
print(f"Portfolio Sharpe Ratio: {sharpe_ratio:.2f}")
