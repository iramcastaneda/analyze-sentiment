import sys
import requests
from textblob import TextBlob
from urllib.parse import urlparse

def is_url(input_str):
    try:
        result = urlparse(input_str)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def fetch_text(input_str):
    if is_url(input_str):
        try:
            response = requests.get(input_str)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL: {e}")
            sys.exit(1)
    else:
        try:
            with open(input_str, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"File not found: {input_str}")
            sys.exit(1)

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

def main():
    if len(sys.argv) != 2:
        print("Usage: python sentiment_analyzer.py <url_or_filepath>")
        sys.exit(1)

    input_str = sys.argv[1]
    text = fetch_text(input_str)
    sentiment = analyze_sentiment(text)
    print(f"Sentiment: {sentiment}")

if __name__ == "__main__":
    main()
