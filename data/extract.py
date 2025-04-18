import praw 
import datetime
import dotenv 
import os 
import analyze
import json 
import requests
import time

dotenv.load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT")
)

def fetch_reddit_link(start_date, end_date):
    base_url = f"https://api.pullpush.io/reddit/submission/search?html_decode=True&subreddit=wallstreetbets&since={start_date}&until={end_date}&size=1000"
    perma_links = []
    raw_reddit = requests.get(base_url)
    raw_data = raw_reddit.json()
    for data in raw_data['data']:
        permalink = data.get("permalink")
        if permalink:
            full_url = f"https://www.reddit.com{permalink}"
            perma_links.append(full_url)

    return perma_links

def format_date(dt):
    return dt.strftime('%d-%m-%Y')

def extract_reddit(submission_url):
    try:
        submission = reddit.submission(url=submission_url)
        submission.comments.replace_more(limit=None)
        all_comments = submission.comments.list()

        created_post_time = datetime.datetime.fromtimestamp(submission.created_utc, datetime.timezone.utc)
        

        status = analyze.analyze_reddit_post(submission.title + submission.selftext)
    

        for comment in all_comments:
            created_at = datetime.datetime.fromtimestamp(comment.created_utc, datetime.timezone.utc)
            post_date = format_date(created_post_time)
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
            print(json.dumps(js))
    except Exception as e:
        print(f"[-] Error processing {submission_url}: {e}")

# Main loop: 3 years of data, day by day
end_date = datetime.datetime.now(datetime.timezone.utc)
start_date = end_date - datetime.timedelta(days=3 * 365)

current_date = start_date
one_day = datetime.timedelta(days=1)

while current_date < end_date:
    since = int(current_date.timestamp())
    until = int((current_date + one_day).timestamp())

    try:
        links = fetch_reddit_link(since, until)
        for link in links:
            extract_reddit(link)
    except Exception as e:
        print(f"[-] Error fetching or extracting posts from {current_date.date()}: {e}")
    
    current_date += one_day
    time.sleep(1)  # Avoid hitting rate limits
