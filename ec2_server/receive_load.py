from flask import Flask, request, jsonify
import psycopg2
import os
import dotenv
import helper
import yfinance as yf
from datetime import datetime, timedelta
dotenv.load_dotenv()

app = Flask(__name__)

# Setup DB connection
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user="postgres",
        password=os.getenv("DB_PASSWORD")
    )

@app.route('/submit', methods=['POST'])
def submit_data():
    try:
        data = request.get_json()

        comment = data.get("Comment")
        score = data.get("Score")
        time = data.get("Time")
        sector = data.get("sector")
        stock_ticker = data.get("stock_ticker")
        sentiment_score = data.get("sentiment_score")

        conn = get_db_connection()
        cur = conn.cursor()

        insert_query = """
            INSERT INTO reddit_comments (comment, score, time, sector, stock_ticker, sentiment_score)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cur.execute(insert_query, (comment, score, time, sector, stock_ticker, sentiment_score))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"status": "success", "message": "Data inserted"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/gethistoricdata', methods=['GET'])
def get_historic_data():
    conn = get_db_connection()
    cur = conn.cursor()

    query = "SELECT * FROM reddit_comments ORDER BY time"
    cur.execute(query)
    rows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]

    data = []
    for row in rows:
        row_dict = dict(zip(colnames, row))
        before_price, after_price = helper.get_cached_prices(row_dict["time"])
        row_dict["before_price"] = before_price
        row_dict["after_price"] = after_price
        data.append(row_dict)

    cur.close()
    conn.close()

    return jsonify(data)

@app.route('/summary_today', methods=['GET'])
def summary_today():
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
        SELECT
            COUNT(*) AS comment_count,
            SUM(score) AS total_score,
            AVG(sentiment_score) AS avg_sentiment
        FROM reddit_comments
        WHERE time::date = CURRENT_DATE;
    """
    cur.execute(query)
    result = cur.fetchone()

    cur.close()
    conn.close()

    return jsonify({
        "comment_count": result[0],
        "total_score": result[1],
        "avg_sentiment": float(result[2]) if result[2] is not None else None
    })


@app.route('/predict_ticker', methods=['GET'])
def get_ticker():
     pass
@app.route('/get_overall_ticker', methods=['GET'])
def get_overall_ticker():
    ticker_symbol = request.args.get('ticker')

    if not ticker_symbol:
        return jsonify({"error": "Ticker symbol is required. Example: /get_overall_ticker?ticker=AAPL"}), 400

    try:
        ticker = yf.Ticker(ticker_symbol.upper())
        end = datetime.today()
        start = end - timedelta(days=7)  # buffer for weekends

        hist = ticker.history(start=start, end=end)
        closes = hist["Close"].tail(4)

        # Convert to dict with dates as string
        result = {date.strftime("%Y-%m-%d"): round(price, 2) for date, price in closes.items()}

        return jsonify({
            "ticker": ticker_symbol.upper(),
            "last_4_days_closing": result
        })
    except Exception as e:
        return jsonify({"error": f"Failed to fetch data: {str(e)}"}), 500




@app.route('/predict_QQQ', method=['GET'])
def get_QQQ():
    pass 

@app.route('/get_QQQ', method=['GET'])
def get_sector():
    pass

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
