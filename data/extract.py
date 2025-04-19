import praw
import datetime
import dotenv
import os
import analyze
import json
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

dotenv.load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT")
)

API_ENDPOINT = "http://3.145.78.241:5000/submit"
subreddits = ["stocks", "options", "investing"]

def fetch_reddit_link(start_date, end_date, subreddit):
    base_url = (
        f"https://api.pullpush.io/reddit/submission/search"
        f"?html_decode=True&subreddit={subreddit}"
        f"&since={start_date}&until={end_date}&size=1000"
    )
    perma_links = []
    try:
        response = requests.get(base_url)
        raw_data = response.json()
        for data in raw_data.get('data', []):
            permalink = data.get("permalink")
            if permalink:
                perma_links.append(f"https://www.reddit.com{permalink}")
    except Exception as e:
        print(f"[-] Failed to fetch links from r/{subreddit}: {e}")
    return perma_links

def format_date(dt):
    return dt.strftime('%d-%m-%Y')

def extract_reddit(submission_url):
    try:
        submission = reddit.submission(url=submission_url)

        if submission.score < 50:
            return

        submission.comments.replace_more(limit=0)
        top_comments = submission.comments[:10]

        created_post_time = datetime.datetime.fromtimestamp(
            submission.created_utc, datetime.timezone.utc
        )
        post_date = format_date(created_post_time)

        for comment in top_comments:
            if comment.score < 50:
                continue
            created_at = datetime.datetime.fromtimestamp(comment.created_utc, datetime.timezone.utc)
            comment_date = format_date(created_at)
            if post_date != comment_date:
                continue

            status = analyze.analyze_reddit_post(comment.body)
            sector = status["sector"]
            stock_ticker = status["stock_ticker"]
            sentiment = status["sentiment_score"]

            js = {
                "Comment": comment.body,
                "Score": comment.score,
                "Time": str(created_at),
                "sector": sector,
                "stock_ticker": stock_ticker,
                "sentiment_score": sentiment
            }

            print("\n--- Reddit Comment ---")
            print("Comment:", comment.body)
            print("Score:", comment.score)
            print("Time:", created_at)
            print("Sector:", sector)
            print("Stock Ticker:", stock_ticker)
            print("Sentiment Score:", sentiment)

            # Send each comment individually
            try:
                res = requests.post(API_ENDPOINT, json=js)
                print(f"[✓] POST → {res.status_code}")
            except Exception as e:
                print(f"[!] POST failed: {e}")

    except Exception as e:
        print(f"[-] Error processing submission: {e}")

# Main loop: 1 year of data, weekly chunks
end_date = datetime.datetime.now(datetime.timezone.utc)
start_date = end_date - datetime.timedelta(days=365)
current_date = start_date
interval = datetime.timedelta(days=7)

executor = ThreadPoolExecutor(max_workers=10)

while current_date < end_date:
    since = int(current_date.timestamp())
    until = int((current_date + interval).timestamp())

    for sub in subreddits:
        try:
            print(f"\n[📥] Fetching r/{sub} posts from {datetime.datetime.fromtimestamp(since).date()} to {datetime.datetime.fromtimestamp(until).date()}")
            links = fetch_reddit_link(since, until, sub)
            futures = [executor.submit(extract_reddit, link) for link in links]

            # Wait for all threads to finish before continuing to next week
            for future in as_completed(futures):
                future.result()

        except Exception as e:
            print(f"[-] Error fetching or extracting from r/{sub}: {e}")

    current_date += interval
    time.sleep(1)
