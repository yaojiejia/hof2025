import torch
import numpy as np
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

def load_model():
    tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
    model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
    return tokenizer, model


def analyze_sentiment(text, tokenizer, model):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    
    with torch.no_grad():
        outputs = model(**inputs)
        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        
    sentiment_score = predictions.detach().numpy()
    sentiment_class = np.argmax(sentiment_score, axis=1)[0]
    
    sentiment_mapping = {0: "negative", 1: "neutral", 2: "positive"}
    sentiment = sentiment_mapping[sentiment_class]
    
    
    return {
        "sentiment": sentiment
    }


def analyze_reddit_post(texts):
    tokenizer, model = load_model()

    sentiment_result = analyze_sentiment(texts, tokenizer, model)
    
    print(sentiment_result)

analyze_reddit_post("Powell indicates tariffs could pose a challenge for the Fed between controlling inflation and supporting economic growth ")