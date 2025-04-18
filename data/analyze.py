import requests
import json
import re

def analyze_reddit_post(post_text: str):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "gemma3",
        "prompt": "Analyze this wallstreetbets post. Return JSON with these keys: sector, stock_ticker, and sentiment_score (a number from -1.0 to 1.0 where -1.0 is very negative, 0 is neutral, and 1.0 is very positive). Use N/A for sector or stock_ticker if uncertain. ONLY RETURN JSON. NO REASONING OR EXPLANATIONS. Post: " + post_text,
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload)
        response_data = response.json()
        
        if "response" in response_data:
            json_match = re.search(r'```(?:json)?(.*?)```', response_data["response"], re.DOTALL)
            
            if json_match:
                json_text = json_match.group(1).strip()
                try:
                    return json.loads(json_text)
                except json.JSONDecodeError:
                    print("Failed to parse JSON directly, trying fallback")
            
            if "{" in response_data["response"] and "}" in response_data["response"]:
                try:
                    start = response_data["response"].find("{")
                    end = response_data["response"].rfind("}") + 1
                    json_text = response_data["response"][start:end]
                    return json.loads(json_text)
                except json.JSONDecodeError:
                    print("Failed to parse JSON with fallback")
            
            # Default with sentiment score
            return {"sector": "N/A", "stock_ticker": "N/A", "sentiment_score": 0.0}
        else:
            print("Unexpected response format")
            return {"sector": "N/A", "stock_ticker": "N/A", "sentiment_score": 0.0}
            
    except Exception as e:
        print(f"Error analyzing post: {e}")
        return {"sector": "N/A", "stock_ticker": "N/A", "sentiment_score": 0.0}

# Example usage
if __name__ == "__main__":
    post = "What happens when Trump eventually fires/replaces Powell?"
    result = analyze_reddit_post(post)
    print(json.dumps(result, indent=2))