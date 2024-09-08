import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
from scipy.optimize import minimize


def load_data():
    tickers_df = pd.read_csv('../datasets/stockprices/Cleaned_Adjusted_Price_report.csv')
    index_df = pd.read_csv('../datasets/indexes/total_index.csv')
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


def compare_initial_optimized_portfolios(ticker_returns, mean_returns, cov_matrix, initial_weights, optimal_weights, risk_free_rate=0):
    initial_weights_array = np.array([initial_weights.get(ticker, 0) for ticker in ticker_returns.columns])

    initial_return, initial_stddev, initial_sharpe, _ = calculate_portfolio_performance(
        initial_weights_array, ticker_returns, mean_returns, cov_matrix, risk_free_rate)

    optimized_return, optimized_stddev, optimized_sharpe, _ = calculate_portfolio_performance(
        optimal_weights, ticker_returns, mean_returns, cov_matrix, risk_free_rate)

    comparison_data = {
        'Metric': ['Expected Return (%)', 'Risk (Std Dev) (%)', 'Sharpe Ratio'],
        'Initial Portfolio': [f'{initial_return:.2f}', f'{initial_stddev:.2f}', f'{initial_sharpe:.2f}'],
        'Optimized Portfolio': [f'{optimized_return:.2f}', f'{optimized_stddev:.2f}', f'{optimized_sharpe:.2f}']
    }

    comparison_df = pd.DataFrame(comparison_data)

    fig, ax = plt.subplots(figsize=(8, 2))  # Adjust the size to fit the table
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=comparison_df.values, colLabels=comparison_df.columns, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.5, 1.5)
    plt.title("Comparison of Initial and Optimized Portfolio Performance")
    plt.show()


tickers_df, index_df = load_data()

initial_weights_dict = {
    'کماسه1': 0.3,
    'شتران1': 0.1,
    'ولغدر1': 0.6
}

tickers_to_include = list(initial_weights_dict.keys())

ticker_returns, index_returns = calculate_returns(tickers_df, index_df, tickers_to_include)
mean_returns, cov_matrix = calculate_stats(ticker_returns)
optimal_weights = optimize_portfolio(ticker_returns, mean_returns, cov_matrix, initial_weights_dict, risk_free_rate=0)
portfolio_return, portfolio_stddev, sharpe_ratio, portfolio_cum_returns = calculate_portfolio_performance(
    optimal_weights, ticker_returns, mean_returns, cov_matrix)

plot_cumulative_returns(portfolio_cum_returns, index_returns)
plot_risk_return_comparison(ticker_returns, mean_returns)

compare_initial_optimized_portfolios(ticker_returns, mean_returns, cov_matrix, initial_weights_dict, optimal_weights)

print("Optimal Weights:", optimal_weights)
print(f"Expected Portfolio Return: {portfolio_return:.2f}%")
print(f"Portfolio Risk (Std Dev): {portfolio_stddev:.2f}%")
print(f"Portfolio Sharpe Ratio: {sharpe_ratio:.2f}")
