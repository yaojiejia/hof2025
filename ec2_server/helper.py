import yfinance as yf
from datetime import datetime, timedelta

def get_prices_around_time(comment_time_str):
    try:
        comment_time = datetime.strptime(comment_time_str, "%a, %d %b %Y %H:%M:%S %Z")

        ticker = yf.Ticker("QQQ")  
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