from flask import Flask, request, jsonify
import psycopg2
import os
import dotenv
import helper
import yfinance as yf
from datetime import datetime, timedelta
import joblib

dotenv.load_dotenv()
model = joblib.load('gbt_model.pkl')

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

@app.route('/predict_today', methods=['GET'])
def predict_today():
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
        SELECT
            SUM(score) AS total_score,
            AVG(sentiment_score) AS avg_sentiment
        FROM reddit_comments
        WHERE time::date = CURRENT_DATE - INTERVAL '1 day';
    """
    cur.execute(query)
    result = cur.fetchone()
    cur.close()
    conn.close()

    total_score = result[0] or 0
    avg_sentiment = float(result[1]) if result[1] is not None else 0

    x_new = [[total_score, avg_sentiment]]
    prediction = model.predict(x_new)[0]

    return jsonify({
        "total_score": total_score,
        "avg_sentiment": avg_sentiment,
        "prediction": float(prediction)
    })


@app.route('/predict_ticker', methods=['GET'])
def predict_ticker():

    ticker_param = request.args.get("ticker")

    if not ticker_param:
        return jsonify({"error": "Please provide a ticker. Example: /predict_ticker?ticker=AAPL"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    query = """
        SELECT
            SUM(score) AS total_score,
            AVG(sentiment_score) AS avg_sentiment
        FROM reddit_comments
        WHERE time::date = CURRENT_DATE - INTERVAL '1 day'
          AND stock_ticker = %s;
    """
    cur.execute(query, (ticker_param.upper(),))
    result = cur.fetchone()
    cur.close()
    conn.close()

    total_score = result[0]
    avg_sentiment = result[1]

    if total_score is None or avg_sentiment is None:
        return jsonify({
            "ticker": ticker_param.upper(),
            "message": "no information for this ticker today"
        }), 200

    x_new = [[total_score, avg_sentiment]]
    prediction = model.predict(x_new)[0]

    return jsonify({
        "ticker": ticker_param.upper(),
        "total_score": total_score,
        "avg_sentiment": float(avg_sentiment),
        "prediction": float(prediction)
    })



# @app.route('/predict_ticker', methods=['GET'])
# def get_ticker():
#      pass
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


@app.route('/predict_sector', methods=['GET'])
def predict_sector():

    sector_param = request.args.get("sector")

    if not sector_param:
        return jsonify({"error": "Please provide a sector. Example: /predict_sector?sector=Technology"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    query = """
        SELECT
            SUM(score) AS total_score,
            AVG(sentiment_score) AS avg_sentiment
        FROM reddit_comments
        WHERE time::date = CURRENT_DATE - INTERVAL '1 day'
          AND sector = %s;
    """
    cur.execute(query, (sector_param,))
    result = cur.fetchone()
    cur.close()
    conn.close()

    total_score = result[0]
    avg_sentiment = result[1]

    if total_score is None or avg_sentiment is None:
        return jsonify({
            "sector": sector_param,
            "message": "no information for this sector yesterday"
        }), 200

    x_new = [[total_score, avg_sentiment]]
    prediction = model.predict(x_new)[0]

    return jsonify({
        "sector": sector_param,
        "total_score": total_score,
        "avg_sentiment": float(avg_sentiment),
        "prediction": float(prediction)
    })

@app.route('/market_summary', methods=['GET'])
def market_summary():
    conn = get_db_connection()
    cur = conn.cursor()

    # 1. Overall state (QQQ)
    cur.execute("""
        SELECT SUM(score), AVG(sentiment_score)
        FROM reddit_comments
        WHERE time::date = CURRENT_DATE - INTERVAL '1 day'
    """)
    result = cur.fetchone()
    qqq_score = result[0] or 0
    qqq_sent = float(result[1]) if result[1] is not None else 0
    qqq_pred = float(model.predict([[qqq_score, qqq_sent]])[0])

    # 2. Top sector (based on ML prediction)
    cur.execute("""
        SELECT sector, SUM(score) AS total_score, AVG(sentiment_score) AS avg_sent
        FROM reddit_comments
        WHERE time::date = CURRENT_DATE - INTERVAL '1 day'
        GROUP BY sector
    """)
    sectors = cur.fetchall()
    sector_preds = []
    for sector, total_score, avg_sent in sectors:
        if total_score is not None and avg_sent is not None:
            pred = float(model.predict([[total_score, avg_sent]])[0])
            sector_preds.append((sector, pred, total_score, avg_sent))

    top_gain_sec = max(sector_preds, key=lambda x: x[1], default=None)
    top_lose_sec = min(sector_preds, key=lambda x: x[1], default=None)

    # 3. Top stock (based on ML prediction)
    cur.execute("""
        SELECT stock_ticker, SUM(score) AS total_score, AVG(sentiment_score) AS avg_sent
        FROM reddit_comments
        WHERE time::date = CURRENT_DATE - INTERVAL '1 day'
        GROUP BY stock_ticker
    """)
    stocks = cur.fetchall()
    stock_preds = []
    for ticker, total_score, avg_sent in stocks:
        if total_score is not None and avg_sent is not None:
            pred = float(model.predict([[total_score, avg_sent]])[0])
            stock_preds.append((ticker, pred, total_score, avg_sent))

    top_gain_stock = max(stock_preds, key=lambda x: x[1], default=None)
    top_lose_stock = min(stock_preds, key=lambda x: x[1], default=None)

    cur.close()
    conn.close()

    return jsonify({
        "state": qqq_pred,
        "top_gain_sec": {
            "sector": top_gain_sec[0],
            "prediction": top_gain_sec[1],
            "score": top_gain_sec[2],
            "avg_sentiment": top_gain_sec[3]
        } if top_gain_sec else None,
        "top_gain_stock": {
            "ticker": top_gain_stock[0],
            "prediction": top_gain_stock[1],
            "score": top_gain_stock[2],
            "avg_sentiment": top_gain_stock[3]
        } if top_gain_stock else None,
        "top_lose_sec": {
            "sector": top_lose_sec[0],
            "prediction": top_lose_sec[1],
            "score": top_lose_sec[2],
            "avg_sentiment": top_lose_sec[3]
        } if top_lose_sec else None,
        "top_lose_stock": {
            "ticker": top_lose_stock[0],
            "prediction": top_lose_stock[1],
            "score": top_lose_stock[2],
            "avg_sentiment": top_lose_stock[3]
        } if top_lose_stock else None,
    })



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

