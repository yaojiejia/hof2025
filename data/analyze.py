import dotenv
import os
from openai import OpenAI
import sys
import json

dotenv.load_dotenv()

OPENAI_KEY = os.getenv("OPENAI")


def analyze_reddit_post(post_text: str):

    client = OpenAI(api_key=OPENAI_KEY)

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": "Analyze this wallstreetbets post. Return JSON with keys: sector, stock_ticker, sentiment (positive/negative). Use N/A if uncertain.\n\nPost:\n" + post_text
            }
        ]
    )
    
    js = {"sector": "N/A", "stock_ticker": "N/A", "sentiment": "N/A"}
    try:
        js = json.loads(completion.choices[0].message.content)
    except Exception as e:
        print(e)
    return js

