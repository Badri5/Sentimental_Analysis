# =============================================================================
# IMPORTS
# =============================================================================
import os
import json
import sqlite3
import requests
import smtplib
from email.message import EmailMessage
import time

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# For the ML pipeline (NLP)
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# For Twitter simulation (we import tweepy even if not used for live streaming)
import tweepy

# =============================================================================
# COMMON FUNCTION: Send Email Notification
# =============================================================================
def send_email_notification(subject, message, to_email, attachment_path=None):
    """
    Sends an email via Gmail SMTP.
    If attachment_path is provided, attaches a file (expected as PDF).
    Update sender credentials as needed.
    """
    sender_email = "badrinadhvhs@gmail.com"  # Replace with your email
    sender_password = os.getenv("EMAIL_PASSWORD")    # Replace with your app password
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # TLS port

    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(message)

    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, "rb") as f:
            file_data = f.read()
            file_name = os.path.basename(attachment_path)
        if file_name.lower().endswith(".pdf"):
            msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)
        else:
            msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure connection
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("Error sending email:", e)

# =============================================================================
# PART 1: Azure Cognitive Services Pipeline
# =============================================================================
def batch_documents(documents, batch_size=10):
    for i in range(0, len(documents), batch_size):
        yield documents[i:i + batch_size]

def analyze_sentiment():
    print("Running Azure sentiment analysis...")
    # Replace with your valid Azure endpoint and API key
    endpoint = "https://sentimentanalysisapi2025.cognitiveservices.azure.com/"
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


headers = {"Ocp-Apim-Subscription-Key": api_key, "Content-Type": "application/json"}
    url = endpoint.rstrip("/") + "/text/analytics/v3.0/sentiment"
    
    all_documents = [
        {"id": "1", "language": "en", "text": "I love working with Azure!"},
        {"id": "2", "language": "en", "text": "This is a challenging problem to solve."},
        {"id": "3", "language": "en", "text": "The new update is fantastic."},
        {"id": "4", "language": "en", "text": "I am not happy with the recent changes."},
        {"id": "5", "language": "en", "text": "The support team was very helpful."},
        {"id": "6", "language": "en", "text": "The interface is confusing and hard to use."},
        {"id": "7", "language": "en", "text": "I appreciate the fast response from customer support."},
        {"id": "8", "language": "en", "text": "The new feature is quite useful and efficient."},
        {"id": "9", "language": "en", "text": "It was difficult to navigate through the settings."},
        {"id": "10", "language": "en", "text": "It is raining today."},
        {"id": "11", "language": "en", "text": "The meeting is scheduled for 3 PM."},
        {"id": "12", "language": "en", "text": "The report is due next week."},
        {"id": "13", "language": "en", "text": "There are 24 hours in a day."},
        {"id": "14", "language": "en", "text": "The sky is clear today."}
    ]
    original_text = {doc["id"]: doc["text"] for doc in all_documents}
    combined_response = {"documents": []}
    for batch in batch_documents(all_documents, batch_size=10):
        print(f"\nProcessing a batch of {len(batch)} document(s)...")
        body = {"documents": batch}
        try:
            response = requests.post(url, headers=headers, json=body)
            response.raise_for_status()
            batch_result = response.json()
            print("Batch API response:", json.dumps(batch_result, indent=2))
            for doc in batch_result.get("documents", []):
                doc["text"] = original_text.get(doc["id"], "")
                combined_response["documents"].append(doc)
        except requests.exceptions.RequestException as e:
            print(f"API request error: {e}")
            if e.response is not None:
                print("Response content:", e.response.text)
    return combined_response

def save_to_database(data):
    db_path = os.path.join(os.getcwd(), "sentiment_analysis.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS SentimentResults (
            id TEXT,
            text TEXT,
            sentiment TEXT
        )
    ''')
    for document in data.get("documents", []):
        if "id" in document and "text" in document:
            cursor.execute('''
                INSERT INTO SentimentResults (id, text, sentiment)
                VALUES (?, ?, ?)
            ''', (document["id"], document["text"], document.get("sentiment", None)))
            print(f"Saved document to DB: {document}")
        else:
            print(f"Document missing keys: {document}")
    conn.commit()
    conn.close()
    print(f"Results saved to database: {db_path}")

def create_interactive_pie_chart(data):
    sentiments = [doc.get("sentiment", "N/A") for doc in data.get("documents", [])]
    sentiment_counts = pd.Series(sentiments).value_counts().reset_index()
    sentiment_counts.columns = ["Sentiment", "Count"]
    fig = px.pie(sentiment_counts, names="Sentiment", values="Count", title="Sentiment Distribution")
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.show()

def generate_pdf_report(data):
    """
    Generates a PDF report for the Azure pipeline as a table (ID, Text, Sentiment).
    """
    pdf_path = os.path.join(os.getcwd(), "sentiment_report.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]
    table_data = [["ID", "Text", "Sentiment"]]
    for document in data.get("documents", []):
        review_text = document.get("text", "").replace(",", " ")
        doc_id = document.get("id", "")
        sentiment = document.get("sentiment", "N/A")
        para_text = Paragraph(review_text, styleN)
        table_data.append([doc_id, para_text, sentiment])
    table = Table(table_data, colWidths=[50, 350, 100])
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    elements = [Paragraph("Azure Sentiment Analysis Report", styles["Title"]),
                Spacer(1, 12),
                table]
    doc.build(elements)
    print(f"PDF report generated: {pdf_path}")
    return pdf_path

def azure_pipeline():
    result = analyze_sentiment()
    if result:
        print("\nCombined API Results:", json.dumps(result, indent=2))
        save_to_database(result)
        create_interactive_pie_chart(result)
        pdf_report_path = generate_pdf_report(result)
        send_email_notification(
            subject="Sentiment Analysis Report Ready (Azure Pipeline)",
            message=("Hello,\n\nThe sentiment analysis report has been generated using Azure Cognitive Services. "
                     "Please find the attached report.\n\nRegards,\nSentiment Analysis System"),
            to_email="abadrinadh55555@gmail.com",
            attachment_path=pdf_report_path
        )

# =============================================================================
# PART 2: ML-Based Sentiment Analysis Pipeline
# =============================================================================
def load_dataset(filename):
    df = pd.read_csv(filename, delimiter='\t')
    print("First 5 rows of the dataset:")
    print(df.head())
    print("\nDataset shape:", df.shape)
    print(df.info())
    return df

def perform_ml_sentiment_analysis(df):
    X = df['Review']
    y = df['Liked']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    tfidf = TfidfVectorizer(stop_words='english', max_features=1500)
    X_train_tfidf = tfidf.fit_transform(X_train)
    X_test_tfidf = tfidf.transform(X_test)
    classifier = LogisticRegression()
    classifier.fit(X_train_tfidf, y_train)
    y_pred = classifier.predict(X_test_tfidf)
    
    acc = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    cr = classification_report(y_test, y_pred)
    
    print("\nML Model Accuracy: {:.2f}%".format(acc * 100))
    print("\nML Confusion Matrix:")
    print(cm)
    print("\nML Classification Report:")
    print(cr)
    
    return classifier, tfidf, acc, cm, cr

def generate_ml_pdf_report(df, accuracy_value, conf_matrix, class_report):
    """
    Generates a detailed PDF report for the ML pipeline in three sections.
    """
    pdf_path = os.path.join(os.getcwd(), "ml_sentiment_report.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]

    elements = []

    # Section 1 - Dataset Details
    dataset_title = Paragraph("Dataset Details", styles["Heading1"])
    elements.append(dataset_title)
    elements.append(Spacer(1, 12))
    dataset_data = [["Review", "Liked"]]
    preview_df = df.head()
    for index, row in preview_df.iterrows():
        clean_review = str(row["Review"]).replace(",", " ")
        dataset_data.append([Paragraph(clean_review, styleN), Paragraph(str(row["Liked"]), styleN)])
    dataset_table = Table(dataset_data, colWidths=[400, 100])
    dataset_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(dataset_table)
    elements.append(Spacer(1, 6))
    shape_text = Paragraph(f"Dataset Shape: {df.shape[0]} rows x {df.shape[1]} columns", styleN)
    elements.append(shape_text)
    elements.append(Spacer(1, 24))

    # Section 2 - Overall Performance & Confusion Matrix
    overall_title = Paragraph("Overall Performance & Confusion Matrix", styles["Heading1"])
    elements.append(overall_title)
    elements.append(Spacer(1, 12))
    perf_data = [["Metric", "Value"], ["Overall Accuracy", f"{accuracy_value * 100:.2f}%"]]
    perf_table = Table(perf_data, colWidths=[200, 300])
    perf_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTSIZE', (0,0), (-1,-1), 10)
    ]))
    elements.append(perf_table)
    elements.append(Spacer(1, 12))
    cm_title = Paragraph("Confusion Matrix", styles["Heading2"])
    elements.append(cm_title)
    tn, fp_val = conf_matrix[0]
    fn, tp_val = conf_matrix[1]
    cm_table_data = [
        ["", "Predicted 0", "Predicted 1"],
        ["Actual 0", str(tn), str(fp_val)],
        ["Actual 1", str(fn), str(tp_val)]
    ]
    cm_table = Table(cm_table_data, colWidths=[100,150,150])
    cm_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('BACKGROUND', (0,0), (0,-1), colors.lightgrey),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTSIZE', (0,0), (-1,-1), 10)
    ]))
    elements.append(cm_table)
    elements.append(Spacer(1, 24))

    # Section 3 - Detailed Classification Report
    report_title = Paragraph("Detailed Classification Report", styles["Heading1"])
    elements.append(report_title)
    elements.append(Spacer(1, 12))
    cr_lines = class_report.splitlines()
    cr_table_data = []
    header = ["Class", "Precision", "Recall", "F1-Score", "Support"]
    cr_table_data.append(header)
    for line in cr_lines:
        parts = line.split()
        if len(parts) == 5:
            cr_table_data.append(parts)
    cr_table = Table(cr_table_data, colWidths=[80,100,100,100,100])
    cr_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTSIZE', (0,0), (-1,-1), 10)
    ]))
    elements.append(cr_table)

    doc.build(elements)
    print(f"ML PDF report generated: {pdf_path}")
    return pdf_path

def ml_pipeline():
    dataset_filename = "Restaurant_Reviews.tsv"  # Make sure this file is in the folder.
    df = load_dataset(dataset_filename)
    classifier, tfidf_transformer, ml_acc, ml_cm, ml_cr = perform_ml_sentiment_analysis(df)
    summary_message = (
        f"Restaurant Reviews Sentiment Analysis Summary:\nOverall Model Accuracy (on test set): {ml_acc * 100:.2f}%"
    )
    print("\nML Email Summary:")
    print(summary_message)
    ml_pdf_path = generate_ml_pdf_report(df, ml_acc, ml_cm, ml_cr)
    send_email_notification(
        subject="Restaurant Reviews Sentiment Analysis Report (ML Pipeline)",
        message=summary_message,
        to_email="abadrinadh55555@gmail.com",
        attachment_path=ml_pdf_path
    )

# =============================================================================
# PART 3: Real-time Twitter Analysis with Integrated Sentiment Analysis 
# (Simulated, Animated Narrative Dashboard, PDF Report, and Email)
# =============================================================================
def load_sentiment_model():
    """
    Loads and trains the sentiment model using the Restaurant Reviews dataset.
    Returns the trained classifier and TF-IDF transformer.
    """
    print("Loading sentiment model from Restaurant Reviews dataset...")
    df = load_dataset("Restaurant_Reviews.tsv")
    classifier, tfidf, acc, cm, cr = perform_ml_sentiment_analysis(df)
    print("Sentiment model loaded with accuracy: {:.2f}%".format(acc * 100))
    return classifier, tfidf

def generate_twitter_pdf_report(sample_tweets, sentiment_results):
    """
    Generates a PDF report containing:
      - A table of each tweet with its predicted sentiment.
      - A summary table with aggregated sentiment counts.
    """
    pdf_path = os.path.join(os.getcwd(), "twitter_sentiment_report.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]
    
    elements = []
    elements.append(Paragraph("Real-Time Twitter Sentiment Analysis Report", styles["Title"]))
    elements.append(Spacer(1, 12))
    
    # Table 1: Tweet Details
    tweet_table_data = [["Tweet", "Predicted Sentiment"]]
    for tweet, sentiment in zip(sample_tweets, sentiment_results):
        tweet_table_data.append([Paragraph(tweet, styleN), sentiment])
    tweet_table = Table(tweet_table_data, colWidths=[400, 150])
    tweet_table.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 1, colors.black),
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("ALIGN", (0,0), (-1,0), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("FONTSIZE", (0,0), (-1,-1), 10)
    ]))
    elements.append(Paragraph("Tweet Details", styles["Heading2"]))
    elements.append(Spacer(1, 12))
    elements.append(tweet_table)
    elements.append(Spacer(1, 24))
    
    # Table 2: Aggregated Sentiment Summary
    pos_count = sentiment_results.count("Positive")
    neg_count = sentiment_results.count("Negative")
    summary_table_data = [["Sentiment", "Count"],
                          ["Positive", pos_count],
                          ["Negative", neg_count]]
    summary_table = Table(summary_table_data, colWidths=[200, 200])
    summary_table.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 1, colors.black),
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("FONTSIZE", (0,0), (-1,-1), 10)
    ]))
    elements.append(Paragraph("Aggregated Sentiment Summary", styles["Heading2"]))
    elements.append(Spacer(1, 12))
    elements.append(summary_table)
    
    doc.build(elements)
    print(f"Twitter sentiment PDF report generated: {pdf_path}")
    return pdf_path

def twitter_pipeline():
    """
    Simulates real-time Twitter streaming for the keyword 'restaurant'.
    For each simulated tweet, uses the sentiment model to predict sentiment,
    generates an animated narrative dashboard, and sends a PDF report via email.
    """
    # Load the sentiment model.
    classifier, tfidf = load_sentiment_model()
    
    print("Simulated Twitter Pipeline: Streaming tweets for keyword 'restaurant'")
    sample_tweets = [
        "I love this restaurant! The food is amazing.",
        "Service at the restaurant could be better.",
        "Not recommended – the food was underwhelming.",
        "Amazing ambiance and delicious food. Will come back!",
        "The restaurant experience was just okay."
    ]
    
    sentiment_results = []
    for tweet in sample_tweets:
        tweet_vector = tfidf.transform([tweet])
        prediction = classifier.predict(tweet_vector)[0]
        label = "Positive" if prediction == 1 else "Negative"
        sentiment_results.append(label)
        print("Tweet received:", tweet)
        print("Predicted Sentiment:", label)
        time.sleep(2)  # Simulate real-time delay
    
    pos_count = sentiment_results.count("Positive")
    neg_count = sentiment_results.count("Negative")
    print("\nAggregated Sentiment:")
    print("Positive:", pos_count, "Negative:", neg_count)
    if neg_count > pos_count:
        print("Alert: Majority negative sentiment detected!")
    
    # Animated narrative dashboard: simulate two phases ("Before" and "After").
    # "Before" is a simulated baseline, "After" are the current counts.
    df_anim = pd.DataFrame({
        "Sentiment": ["Positive", "Negative", "Positive", "Negative"],
        "Count": [2, 3, pos_count, neg_count],
        "Phase": ["Before", "Before", "After", "After"]
    })
    fig_anim = px.bar(
        df_anim,
        x="Sentiment",
        y="Count",
        color="Sentiment",
        animation_frame="Phase",
        range_y=[0, max(3, pos_count, neg_count) + 1],
        title="Animated Sentiment Change Simulation"
    )
    fig_anim.update_layout(title_x=0.5)
    # Add a custom annotation if positive sentiment increases.
    if pos_count > 2:
        fig_anim.add_annotation(text="Positive sentiment improved!",
                                x=0.2, y=pos_count, showarrow=True, arrowhead=2)
    fig_anim.show()
    
    # Generate PDF report for the Twitter analysis.
    twitter_pdf_path = generate_twitter_pdf_report(sample_tweets, sentiment_results)
    
    # Send the PDF report via email.
    send_email_notification(
        subject="Real-time Twitter Sentiment Analysis Report",
        message=("Hello,\n\nPlease find attached the Real-Time Twitter Sentiment Analysis PDF Report "
                 "with animated narrative insights.\n\nRegards,\nSentiment Analysis System"),
        to_email="abadrinadh55555@gmail.com",
        attachment_path=twitter_pdf_path
    )

# =============================================================================
# MAIN EXECUTION BLOCK
# =============================================================================
if __name__ == "__main__":
    print("Select pipeline to run:")
    print("1 - Azure Cognitive Services Pipeline")
    print("2 - ML-Based Sentiment Analysis (Restaurant Reviews Dataset)")
    print("3 - Run Both Azure & ML Pipelines")
    print("4 - Real-time Twitter Analysis with Integrated Sentiment Analysis (Simulated, Animated Narrative, PDF Report & Email)")
    choice = input("Enter your choice (1/2/3/4): ")
    if choice == "1":
        azure_pipeline()
    elif choice == "2":
        ml_pipeline()
    elif choice == "3":
        azure_pipeline()
        ml_pipeline()
    elif choice == "4":
        twitter_pipeline()
    else:
        print("Invalid choice. Exiting.")
