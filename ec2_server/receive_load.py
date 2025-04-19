from flask import Flask, request, jsonify
import psycopg2
import os
import dotenv

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

    data = [dict(zip(colnames, row)) for row in rows]

    cur.close()
    conn.close()

    return jsonify(data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
