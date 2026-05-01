import requests
import json
import matplotlib.pyplot as plt
from datetime import datetime
import schedule
import time
import os
# Function to perform sentiment analysis
def analyze_sentiment():
    # Set the endpoint URL and API key
    endpoint = "https://sentimentanalysisapi2025.cognitiveservices.azure.com/"
    api_key = os.getenv("AZURE_API_KEY")

    # Headers for the request
    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json"
    }

    # Request body with additional documents to analyze
    body = {
        "documents": [
            {"id": "1", "language": "en", "text": "I love working with Azure!"},
            {"id": "2", "language": "en", "text": "This is a challenging problem to solve."},
            {"id": "3", "language": "en", "text": "The new update is fantastic."},
            {"id": "4", "language": "en", "text": "I am not happy with the recent changes."},
            {"id": "5", "language": "en", "text": "The support team was very helpful."},
            {"id": "6", "language": "en", "text": "The interface is confusing and hard to use."},
            {"id": "7", "language": "en", "text": "I appreciate the fast response from customer support."},
            {"id": "8", "language": "en", "text": "The new feature is quite useful and efficient."},
            {"id": "9", "language": "en", "text": "It was difficult to navigate through the settings."},
            {"id": "10", "language": "en", "text": "Great experience overall, very satisfied with the service."}
            # Add more documents as needed
        ]
    }

    # Make the request to the API
    response = requests.post(f"{endpoint}/text/analytics/v3.0/sentiment", headers=headers, json=body)

    # Parse the JSON response
    sentiment_result = response.json()
    print(json.dumps(sentiment_result, indent=2))

    # Initialize counters for aggregation
    positive_count = 0
    neutral_count = 0
    negative_count = 0

    # Aggregate sentiment counts
    for document in sentiment_result["documents"]:
        sentiment = document["sentiment"]
        if sentiment == "positive":
            positive_count += 1
        elif sentiment == "neutral":
            neutral_count += 1
        elif sentiment == "negative":
            negative_count += 1

    # Print aggregated counts
    print(f"Positive: {positive_count}")
    print(f"Neutral: {neutral_count}")
    print(f"Negative: {negative_count}")

    # Create a bar chart to visualize the sentiment analysis results
    sentiments = ['positive', 'neutral', 'negative']
    counts = [positive_count, neutral_count, negative_count]

    plt.bar(sentiments, counts, color=['green', 'blue', 'red'])
    plt.xlabel('Sentiment')
    plt.ylabel('Count')
    plt.title('Sentiment Analysis Results')
    plt.show()

    # Visualize Trends Over Time: Example Time-Series Data
    dates = [datetime(2023, 1, 1), datetime(2023, 2, 1), datetime(2023, 3, 1)]
    positive_counts = [10, 15, 8]
    neutral_counts = [5, 7, 10]
    negative_counts = [2, 3, 5]

    # Plotting the time series
    plt.plot(dates, positive_counts, label='Positive', color='green')
    plt.plot(dates, neutral_counts, label='Neutral', color='blue')
    plt.plot(dates, negative_counts, label='Negative', color='red')

    plt.xlabel('Date')
    plt.ylabel('Sentiment Count')
    plt.title('Sentiment Trends Over Time')
    plt.legend()
    plt.show()

# Schedule the sentiment analysis to run daily at 9 AM
schedule.every().day.at("09:00").do(analyze_sentiment)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
