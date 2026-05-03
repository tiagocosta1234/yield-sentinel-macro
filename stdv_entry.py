import yfinance as yf
import pandas as pd
import datetime
import pytz
import time

# --- 1. WEEKLY CONFIGURATION (Update this every Sunday) ---
# Format: "YYYY-MM-DD HH:MM" in EST/New York Time
RED_FOLDER_EVENTS = [
    "2026-05-05 10:00",
    "2026-05-08 08:30",
    "2026-05-12 08:30",
    "2026-05-13 08:30",
    "2026-05-14 08:30"
]

# --- 2. STRATEGY PARAMETERS ---
SYMBOL_LIST = ["NQ=F", "MNQ=F"] 
EMA_FAST = 50
LOOKBACK = 20
RISK_USD = 150.0   # $150 Risk for 1 MNQ Contract
REWARD_USD = 450.0 # $450 Reward
MNQ_POINT_VALUE = 2.0

def is_news_active():
    """Checks if current time is within 15 mins of a red folder event."""
    est = pytz.timezone('US/Eastern')
    now_est = datetime.datetime.now(est)
    
    for event_str in RED_FOLDER_EVENTS:
        event_time = est.localize(datetime.datetime.strptime(event_str, "%Y-%m-%d %H:%M"))
        diff_minutes = (event_time - now_est).total_seconds() / 60
        
        # 15 min buffer before and after
        if -15 <= diff_minutes <= 15:
            return True
    return False

def is_market_closing_soon():
    """Lucid Deadline: Must be flat by 4:45 PM EST."""
    est = pytz.timezone('US/Eastern')
    now_est = datetime.datetime.now(est)
    if (now_est.hour == 16 and now_est.minute >= 40) or (now_est.hour == 17):
        return True
    return False

def fetch_live_data():
    for ticker in SYMBOL_LIST:
        try:
            df = yf.download(ticker, period="2d", interval="5m", progress=False)
            if not df.empty and len(df) > 50:
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)
                return df, ticker
        except Exception: continue
    return pd.DataFrame(), None

def compute_live_signal(df):
    d = df.copy()
    d["ema"] = d["Close"].ewm(span=EMA_FAST, adjust=False).mean()
    d["roll_hi"] = d["High"].shift(1).rolling(LOOKBACK).max()
    d["roll_lo"] = d["Low"].shift(1).rolling(LOOKBACK).min()
    
    last_bar, prev_bar = d.iloc[-1], d.iloc[-2]
    
    is_buy = (last_bar["Close"] > last_bar["roll_hi"]) and (last_bar["ema"] > prev_bar["ema"])
    is_sell = (last_bar["Close"] < last_bar["roll_lo"]) and (last_bar["ema"] < prev_bar["ema"])
    
    if is_buy:
        entry = last_bar["Close"]
        return {"Side": "BUY/LONG", "Entry": entry, "Stop": entry - 75, "Target": entry + 225}
    elif is_sell:
        entry = last_bar["Close"]
        return {"Side": "SELL/SHORT", "Entry": entry, "Stop": entry + 75, "Target": entry - 225}
    return None

def run_scout():
    print("\n" + "="*50)
    print("🚀 STDV SCOUT v7.5 - LIVE & PROTECTED")
    print("="*50)

    while True:
        try:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            if is_market_closing_soon():
                print(f"[{timestamp}] ⚠️ Lucid Deadline Near. Paused.")
            elif is_news_active():
                print(f"[{timestamp}] 🛑 RED FOLDER NEWS ALERT. Paused.")
            else:
                data, ticker = fetch_live_data()
                if not data.empty:
                    signal = compute_live_signal(data)
                    if signal:
                        print(f"\n🔥 SIGNAL DETECTED AT {timestamp} 🔥")
                        print(f"ENTRY: {signal['Entry']:.2f} | SL: {signal['Stop']:.2f} | TP: {signal['Target']:.2f}\n")
                    else:
                        print(f"[{timestamp}] Scanning {ticker}... No signal.")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(60)

if __name__ == "__main__":
    run_scout()