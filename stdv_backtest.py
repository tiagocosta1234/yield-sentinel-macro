"""
STDV PO3 BACKTEST - "The Lucid Professional" v7.4
Features: Fixed Risk Math, Time-to-Pass tracking, and simulated Daily Kill Switch.
"""

import numpy as np
import pandas as pd
from scipy.stats import t
import warnings

warnings.filterwarnings("ignore")

# --- 1. Balanced Configuration ---
INITIAL_CAPITAL = 50_000
CONTRACTS_TOTAL = 1      
MNQ_POINT_VALUE = 2.0
COMMISSION_PER_ROUND = 2.10 
SLIPPAGE_PTS = 2.0       

PROP_TARGET = 53_000
PROP_MAX_DRAWDOWN = 2000

# Strategy Params
EMA_FAST = 50
LOOKBACK = 20

# --- 2. Synthetic Market Generation ---
def generate_realistic_nq(seed):
    np.random.seed(seed)
    n = 2000  
    # Generate continuous timestamps to allow the kill switch to function
    dates = pd.date_range("2024-01-01 09:30", periods=n, freq="5min")
    returns = t.rvs(df=3, loc=0.0006, scale=0.012, size=n)
    price = 15_000 * np.exp(np.cumsum(returns))
    rng = np.random.default_rng(seed)
    high = price * (1 + abs(rng.standard_t(3, n) * 0.006))
    low = price * (1 - abs(rng.standard_t(3, n) * 0.006))
    return pd.DataFrame({"High": high, "Low": low, "Close": price}, index=dates)

def compute_signals(df):
    d = df.copy()
    d["ema"] = d["Close"].ewm(span=EMA_FAST, adjust=False).mean()
    d["roll_hi"] = d["High"].shift(1).rolling(LOOKBACK).max()
    d["roll_lo"] = d["Low"].shift(1).rolling(LOOKBACK).min()
    d["buy"] = (d["Close"] > d["roll_hi"]) & (d["ema"] > d["ema"].shift(1))
    d["sell"] = (d["Close"] < d["roll_lo"]) & (d["ema"] < d["ema"].shift(1))
    return d.dropna()

def run_pass_attempt(df):
    d = compute_signals(df)
    equity, position, high_water = INITIAL_CAPITAL, None, INITIAL_CAPITAL
    trades, curve = [], []
    
    RISK_USD = 150.0 
    REWARD_USD = 450.0 
    
    bars_elapsed = 0
    status = "FAILED"

    for i in range(len(d)):
        bars_elapsed += 1
        if equity > high_water: high_water = equity
        
        # Terminal Conditions
        if equity <= (high_water - PROP_MAX_DRAWDOWN):
            return "BLOWN", trades, curve, bars_elapsed
        if equity >= PROP_TARGET:
            return "PASSED", trades, curve, bars_elapsed

        current_time = d.index[i]

        # --- SIMULATED TIME KILL SWITCH ---
        # Force close open positions at 4:40 PM to mimic Lucid rules
        if current_time.hour == 16 and current_time.minute >= 40:
            if position:
                diff = (d["Close"].values[i] - position["entry"]) if position["dir"] == "long" else (position["entry"] - d["Close"].values[i])
                pnl = (diff * MNQ_POINT_VALUE) - COMMISSION_PER_ROUND
                equity += pnl
                trades.append(pnl)
                position = None 
            continue # Skip taking new trades during this dead period

        # Core Trade Logic
        if position:
            diff = (d["Close"].values[i] - position["entry"]) if position["dir"] == "long" else (position["entry"] - d["Close"].values[i])
            pnl = diff * MNQ_POINT_VALUE
            
            if pnl <= -RISK_USD:
                final_pnl = -RISK_USD - COMMISSION_PER_ROUND
                equity += final_pnl
                trades.append(final_pnl)
                position = None
            elif pnl >= REWARD_USD:
                final_pnl = REWARD_USD - COMMISSION_PER_ROUND
                equity += final_pnl
                trades.append(final_pnl)
                position = None
        
        elif d["buy"].values[i]:
            position = {"dir": "long", "entry": d["Close"].values[i] + SLIPPAGE_PTS}
        elif d["sell"].values[i]:
            position = {"dir": "short", "entry": d["Close"].values[i] - SLIPPAGE_PTS}
        
        curve.append(equity)
        
    return status, trades, curve, bars_elapsed

# --- 3. Run Monte Carlo Simulation ---
if __name__ == "__main__":
    SIMULATIONS = 50
    pass_count = 0
    all_trade_counts = []
    all_profit_factors = []
    all_pass_times = []
    
    print(f"Executing v7.4 Monte Carlo ({SIMULATIONS} Runs) with 4:40 PM Kill Switch...")
    
    for s in range(SIMULATIONS):
        df_sim = generate_realistic_nq(seed=np.random.randint(1, 999999))
        result, trades, curve, time_taken = run_pass_attempt(df_sim)
        
        if result == "PASSED":
            pass_count += 1
            all_trade_counts.append(len(trades))
            all_pass_times.append(time_taken)
            
            wins = sum([t for t in trades if t > 0])
            losses = abs(sum([t for t in trades if t < 0]))
            if losses > 0:
                all_profit_factors.append(wins / losses)

    # Output Formatting
    print("\n" + "="*60)
    print(f"       FINAL AUDIT: MNQ PROP EVALUATION (v7.4)")
    print("="*60)
    print(f"Pass Rate                     : {(pass_count/SIMULATIONS)*100:.2f}%")
    print(f"Success Ratio                 : {pass_count} / {SIMULATIONS}")
    print("-" * 60)
    
    if all_trade_counts:
        avg_bars = np.mean(all_pass_times)
        # 138 bars = 1 full RTH session for NQ (9:30 AM - 4:00 PM)
        est_days = avg_bars / 138 
        
        print(f"Avg Trades to Pass            : {np.mean(all_trade_counts):.1f}")
        print(f"Avg Profit Factor             : {np.mean(all_profit_factors):.2f}")
        print(f"Avg Time to Pass (Bars)       : {avg_bars:.1f}")
        print(f"Est. Trading Days to Pass     : {est_days:.1f} Days")
        print("-" * 60)
        
        if est_days < 5:
            print("LUCID NOTE: You may pass faster than 5 days. \nPrepare to trade 1 micro for 'filler' days.")
        else:
            print("LUCID NOTE: Strategy duration naturally fits the 5-day rule.")
    print("="*60)