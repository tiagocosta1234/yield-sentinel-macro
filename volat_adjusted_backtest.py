import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

def run_vol_adjusted_backtest():
    # 1. Config
    ticker = "MNQ=F"
    start_date = "2020-01-01"
    end_date = "2026-04-30"
    initial_capital = 100000
    point_value = 2
    risk_per_trade_usd = 4000 # Your updated high-risk setting
    
    # 2. Data
    data = yf.download(ticker, start=start_date, end=end_date)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    # 3. Indicators & Filters
    data['EMA_Fast'] = data['Close'].ewm(span=10, adjust=False).mean()
    data['EMA_Slow'] = data['Close'].ewm(span=30, adjust=False).mean()
    data['SMA_200'] = data['Close'].rolling(window=200).mean()
    data['ATR'] = (data['High'] - data['Low']).rolling(14).mean()

    # 4. Signal & Sizing (Vectorized)
    data['Signal'] = ((data['EMA_Fast'] > data['EMA_Slow']) & (data['Close'] > data['SMA_200'])).astype(int)
    data['Target_Contracts'] = (risk_per_trade_usd / (data['ATR'].shift(1) * point_value)).fillna(0)
    data['Target_Contracts'] = data['Target_Contracts'].apply(np.round).clip(lower=1, upper=12)

    # 5. PnL & Equity calculation
    data['Point_Change'] = data['Close'].diff()
    data['Daily_PnL'] = data['Signal'].shift(1) * data['Target_Contracts'].shift(1) * data['Point_Change'] * point_value
    data['Strategy_Equity'] = data['Daily_PnL'].cumsum() + initial_capital

    first_valid_idx = data['SMA_200'].first_valid_index()
    data['Buy_Hold_Equity'] = (data['Close'] / data['Close'].loc[first_valid_idx]) * initial_capital

    # 6. Statistics Logic
    clean_data = data.dropna(subset=['SMA_200', 'Strategy_Equity']).copy()
    
    def get_stats(equity_series, signal_series, name, is_strategy=True):
        start_val = equity_series.iloc[0]
        end_val = equity_series.iloc[-1]
        returns = equity_series.pct_change().dropna()
        
        total_ret = ((end_val - start_val) / start_val) * 100
        sharpe = (returns.mean() / returns.std()) * np.sqrt(252) if returns.std() != 0 else 0
        max_dd = ((equity_series - equity_series.cummax()) / equity_series.cummax()).min() * 100
        
        print(f"\n--- {name} Statistics ---")
        print(f"Total Return:      {total_ret:.2f}%")
        print(f"Max Drawdown:      {max_dd:.2f}%")
        print(f"Sharpe Ratio:      {sharpe:.2f}")
        
        if is_strategy:
            entry_indices = signal_series[(signal_series == 1) & (signal_series.shift(1) == 0)].index
            exit_indices = signal_series[(signal_series == 0) & (signal_series.shift(1) == 1)].index
            trade_results = [data.loc[exit_indices[i], 'Close'] > data.loc[entry_indices[i], 'Close'] 
                            for i in range(min(len(entry_indices), len(exit_indices)))]
            win_rate = (sum(trade_results) / len(trade_results) * 100) if trade_results else 0
            print(f"Win Rate:          {win_rate:.2f}% ({len(trade_results)} total trades)")
        
        return max_dd

    strat_dd = get_stats(clean_data['Strategy_Equity'], clean_data['Signal'], "VOL-ADJUSTED STRATEGY")
    bh_dd = get_stats(clean_data['Buy_Hold_Equity'], None, "BUY & HOLD", is_strategy=False)

    # 7. Visualization
    plt.figure(figsize=(12, 6))
    plt.plot(data['Strategy_Equity'], label=f'Strategy (Max DD: {strat_dd:.1f}%)', color='darkgreen', lw=2)
    plt.plot(data['Buy_Hold_Equity'], label=f'Buy & Hold (Max DD: {bh_dd:.1f}%)', color='gray', alpha=0.4, ls='--')
    plt.title(f"MNQ Hunter: Vol-Adjusted Performance (${risk_per_trade_usd} Risk)")
    plt.ylabel("Account Value ($)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.show()

if __name__ == "__main__":
    run_vol_adjusted_backtest()