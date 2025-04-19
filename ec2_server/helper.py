import yfinance as yf
from datetime import datetime, timedelta
from dateutil import parser as dateparser
import time
import pandas as pd
def get_prices_around_time(comment_time_raw):
    time.sleep(1)
    try:
        # Handle both string and datetime input
        if isinstance(comment_time_raw, str):
            comment_time = dateparser.parse(comment_time_raw)
        else:
            comment_time = comment_time_raw

        ticker = yf.Ticker("QQQ")  # Or use "^IXIC"
        history = ticker.history(
            start=comment_time - timedelta(days=3),
            end=comment_time + timedelta(days=3)
        )

        before = history[:comment_time]
        after = history[comment_time:]

        before_price = before["Close"].iloc[-1] if not before.empty else None
        after_price = after["Close"].iloc[0] if not after.empty else None

        return before_price, after_price
    except Exception as e:
        print(f"[!] Error fetching price: {e}")
        return None, None
    

qqq_df = pd.read_csv("qqq_1y_history.csv", parse_dates=["Date"])
qqq_df.set_index("Date", inplace=True)

def get_cached_prices(comment_time):
    try:
        # Ensure it's datetime
        if isinstance(comment_time, str):
            comment_time = pd.to_datetime(comment_time)

        # Find before and after price using nearest trading dates
        before = qqq_df[qqq_df.index <= comment_time]
        after = qqq_df[qqq_df.index > comment_time]

        before_price = before["Close"].iloc[-1] if not before.empty else None
        after_price = after["Close"].iloc[0] if not after.empty else None

        return before_price, after_price
    except Exception as e:
        print(f"[!] Error looking up cached price: {e}")
        return None, None
    

def get_qqq():
    qqq = yf.Ticker("QQQ")
    hist = qqq.history(period="1y", interval="1d")  # daily close price

    # Save to CSV
    hist.to_csv("qqq_1y_history.csv")
