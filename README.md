# 📊 Automated Sentiment Analysis System

A Python-based sentiment analysis system that leverages Azure Cognitive Services to analyze text data and generate insights through visualization, database storage, and automated reporting.

---

## 🚀 Features

* 🔍 Sentiment analysis using Azure Text Analytics API
* ⚡ Batch processing for multiple inputs
* 🗄️ Store results in SQLite database
* 📊 Visualization using Plotly
* 📈 Data aggregation using Pandas
* 📝 PDF report generation using ReportLab
* 📧 Email notification with report attachment
* 🔐 Secure handling of API keys using environment variables
* 🧪 Demo mode when API key is not provided

---

## 🛠️ Tech Stack

* Python
* Azure Text Analytics API
* Pandas
* Plotly
* Matplotlib
* ReportLab
* SQLite
* Requests
* SMTP (Email Automation)

---

## ⚙️ How It Works

1. Text data is processed in batches
2. Azure API analyzes sentiment
3. Results are stored in a database
4. Data is aggregated and visualized
5. A PDF report is generated
6. Report is sent via email

---

## ⚙️ Setup & Run

```bash id="h1w8bc"
python -m pip install requests matplotlib schedule plotly reportlab pandas
```

```bash id="b3ql3p"
set AZURE_API_KEY=your_api_key
set EMAIL_PASSWORD=your_app_password
```

```bash id="u3x0d7"
python automated_sentiment_analysis.py
```

---

## ⚠️ Note

If no API key is provided, the system runs in **demo mode**.

---

## 👤 Author

Badri
