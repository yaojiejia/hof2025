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
    print(base_url)
    raw_reddit = requests.get(base_url)
    raw_data = raw_reddit.json()
    for data in raw_data['data']:
        permalink = data.get("permalink")
        if permalink:
            full_url = f"https://www.reddit.com{permalink}"
            perma_links.append(full_url)

    return perma_links
    
def extract_reddit(submission_url):
    submission = reddit.submission(url=submission_url)

    submission.comments.replace_more(limit=None)

    all_comments = submission.comments.list()

    print("\nSubmission Details:")
    print("Title:", submission.title)
    print("Post Content:", submission.selftext)  
    created_post_time = datetime.datetime.fromtimestamp(submission.created_utc, datetime.timezone.utc)
    print("Posted at:", created_post_time)
    print("Score:", submission.score)

    status = analyze.analyze_reddit_post(submission.title + submission.selftext)
    print(status)
    for comment in all_comments:

        status = analyze.analyze_reddit_post(comment.body)
        print(status)
        sector = status["sector"]
        stock_ticker = status["stock_ticker"]
        sentiment = status["sentiment"]
        print(sector)
        print(stock_ticker)
        print(sentiment)
        created_at = datetime.datetime.fromtimestamp(comment.created_utc, datetime.timezone.utc)
        js = {"Comment": comment.body, "Score": comment.score, "Time": str(created_at), "sector": sector, "stock_ticker": stock_ticker, "sentiment": sentiment}
        json_dict = json.dumps(js)
        print(json_dict)

#extract_reddit("https://www.reddit.com/r/wallstreetbets/comments/1k1pew7/china_is_going_to_meet_with_us_soon/")

# links = fetch_reddit_link("1577854800", "1577941200")
# for link in links:
#     extract_reddit(link)

print(analyze.analyze_reddit_post("What happens when Trump eventually fires/replaces Powell? "))