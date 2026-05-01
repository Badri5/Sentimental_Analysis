import requests
import json
import sqlite3
import os
import pandas as pd
import plotly.express as px
import textwrap  # (unused in the table version, but kept if needed)
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import smtplib
from email.message import EmailMessage

# -------------------------------
# Helper function: batch documents
# -------------------------------
def batch_documents(documents, batch_size=10):
    """
    Generator that yields batches from the list of documents.
    Each batch will contain at most batch_size documents.
    """
    for i in range(0, len(documents), batch_size):
        yield documents[i:i + batch_size]

# -------------------------------
# Function: perform sentiment analysis using batching
# -------------------------------
def analyze_sentiment():
    print("Running sentiment analysis...")
    
    # Set the endpoint URL and API key (Azure Cognitive Services)
    endpoint = "https://sentimentanalysisapi2025.cognitiveservices.azure.com/"
    api_key = os.getenv("AZURE_API_KEY")
    if not api_key:
        print("No API key found. Running in demo mode.")
        return
    
    # Headers for the request
    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json"
    }
    
    # Build the full URL (remove trailing slashes and add sentiment endpoint)
    url = endpoint.rstrip('/') + '/text/analytics/v3.0/sentiment'
    
    # All 14 documents to be analyzed (your reviews)
    all_documents = [
        {"id": "1",  "language": "en", "text": "I love working with Azure!"},
        {"id": "2",  "language": "en", "text": "This is a challenging problem to solve."},
        {"id": "3",  "language": "en", "text": "The new update is fantastic."},
        {"id": "4",  "language": "en", "text": "I am not happy with the recent changes."},
        {"id": "5",  "language": "en", "text": "The support team was very helpful."},
        {"id": "6",  "language": "en", "text": "The interface is confusing and hard to use."},
        {"id": "7",  "language": "en", "text": "I appreciate the fast response from customer support."},
        {"id": "8",  "language": "en", "text": "The new feature is quite useful and efficient."},
        {"id": "9",  "language": "en", "text": "It was difficult to navigate through the settings."},
        {"id": "10", "language": "en", "text": "It is raining today."},
        {"id": "11", "language": "en", "text": "The meeting is scheduled for 3 PM."},
        {"id": "12", "language": "en", "text": "The report is due next week."},
        {"id": "13", "language": "en", "text": "There are 24 hours in a day."},
        {"id": "14", "language": "en", "text": "The sky is clear today."}
    ]
    
    # Map each document id to its original text for later lookup
    original_text = {doc["id"]: doc["text"] for doc in all_documents}
    
    combined_response = {"documents": []}
    
    # Process documents in batches (each batch has at most 10 documents)
    for batch in batch_documents(all_documents, batch_size=10):
        print(f"Processing batch with {len(batch)} document(s)...")
        body = {"documents": batch}
        try:
            response = requests.post(url, headers=headers, json=body)
            response.raise_for_status()  # Raise error if the request failed
            batch_result = response.json()
            print("Batch API request successful.")
            print("Batch API response:", json.dumps(batch_result, indent=2))
            # Merge the API result with the original texts by document ID
            for doc in batch_result.get("documents", []):
                doc["text"] = original_text.get(doc["id"], "")
                combined_response["documents"].append(doc)
        except requests.exceptions.RequestException as e:
            print(f"API request error: {e}")
            if e.response is not None:
                print("Response content:", e.response.text)
    
    return combined_response

# -------------------------------
# Function: save results to an SQLite database
# -------------------------------
def save_to_database(data):
    db_path = os.path.join(os.getcwd(), 'sentiment_analysis.db')
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
    print(f"Results saved to {db_path}")

# -------------------------------
# Function: create interactive pie chart using Plotly
# -------------------------------
def create_interactive_pie_chart(data):
    sentiments = [doc.get("sentiment", "N/A") for doc in data.get("documents", [])]
    sentiment_counts = pd.Series(sentiments).value_counts().reset_index()
    sentiment_counts.columns = ["Sentiment", "Count"]
    fig = px.pie(sentiment_counts, names="Sentiment", values="Count", title="Sentiment Distribution")
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.show()

# -------------------------------
# Function: generate a PDF report in table format using ReportLab Platypus
# -------------------------------
def generate_pdf_report(data):
    pdf_path = os.path.join(os.getcwd(), "sentiment_report.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]

    # Build table data with a header row
    table_data = [["ID", "Text", "Sentiment"]]
    for document in data.get("documents", []):
        doc_id = document.get("id", "")
        text_val = document.get("text", "")
        sentiment = document.get("sentiment", "N/A")
        para_text = Paragraph(text_val, styleN)
        table_data.append([doc_id, para_text, sentiment])
    
    # Create the table with specified column widths
    table = Table(table_data, colWidths=[50, 350, 100])
    table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
    ]))
    
    elements = []
    title = Paragraph("Sentiment Analysis Report", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 12))
    elements.append(table)
    
    # Build the PDF
    doc.build(elements)
    print(f"PDF report generated: {pdf_path}")
    return pdf_path

# -------------------------------
# Function: send email notification with optional attachment
# -------------------------------
def send_email_notification(subject, message, to_email, attachment_path=None):
    sender_email = "badrinadhvhs@gmail.com"         # Your app's sender email.
    sender_password = os.getenv("EMAIL_PASSWORD")            # Your generated app password.
    smtp_server = "smtp.gmail.com"                     # Gmail's SMTP server.
    smtp_port = 587                                  # Port for TLS encryption.

    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.set_content(message)

    # Attach file automatically if provided
    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, "rb") as f:
            file_data = f.read()
            file_name = os.path.basename(attachment_path)
        # Assuming the attachment is a PDF. Otherwise, adjust subtype accordingly.
        if file_name.lower().endswith(".pdf"):
            msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)
        else:
            msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("Error sending email:", e)

# -------------------------------
# Main execution block
# -------------------------------
if __name__ == "__main__":
    result = analyze_sentiment()
    if result:
        print("Combined API Results:", json.dumps(result, indent=2))
        save_to_database(result)
        create_interactive_pie_chart(result)
        pdf_report_path = generate_pdf_report(result)
        
        # Send email with the PDF report attached
        send_email_notification(
            subject="Sentiment Analysis Report Ready",
            message=("Hello,\n\nThe sentiment analysis report has been generated successfully. "
                     "Please find the attached report.\n\nRegards,\nEmail Sender for Sentiment Reports"),
            to_email="abadrinadh55555@gmail.com",
            attachment_path=pdf_report_path
        )
